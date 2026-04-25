"""
Validations as code — Python flavor.

Tool-agnostic: works with any PEP-249 DB-API connection (DuckDB, sqlite3,
psycopg, snowflake-connector, etc.) and with plain pandas DataFrames.

Inspired by ECBS5294: https://github.com/earino/ECBS5294

Usage:
    from validations import (
        assert_pk_unique, assert_not_null, assert_in_set,
        assert_range, assert_fk, assert_row_count_within,
    )

    assert_pk_unique(con, "silver_orders", "order_id")
    assert_not_null(con, "silver_orders", ["order_id", "customer_id"])
    assert_in_set(con, "silver_orders", "status",
                  {"pending", "completed", "cancelled"})
    assert_range(con, "silver_orders", "total_amount", lo=0)
    assert_fk(con, "silver_orders", "customer_id",
              "silver_customers", "customer_id")
"""

from __future__ import annotations

import re
from typing import Iterable


# --- DB-API helpers ---------------------------------------------------------

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _validate_identifier(name: str) -> str:
    """Allow only simple SQL identifiers to avoid injection in snippets."""
    if not _IDENT_RE.match(name):
        raise ValueError(f"Unsafe SQL identifier: {name!r}")
    return name


def _quote_literal(value: object) -> str:
    """Quote SQL literals safely for teaching snippets across DB-API drivers."""
    text = str(value).replace("'", "''")
    return f"'{text}'"


def _scalar(con, sql: str) -> int:
    owns_cursor = hasattr(con, "cursor")
    cur = con.cursor() if owns_cursor else con
    try:
        cur.execute(sql)
        row = cur.fetchone()
        return int(row[0]) if row else 0
    finally:
        if owns_cursor and hasattr(cur, "close"):
            cur.close()


def assert_pk_unique(con, table: str, pk: str) -> None:
    table = _validate_identifier(table)
    pk = _validate_identifier(pk)
    n_rows = _scalar(con, f"SELECT COUNT(*) FROM {table}")
    n_uniq = _scalar(con, f"SELECT COUNT(DISTINCT {pk}) FROM {table}")
    assert n_rows == n_uniq, (
        f"{table}.{pk} not unique: {n_rows} rows, {n_uniq} distinct "
        f"({n_rows - n_uniq} duplicates)"
    )


def assert_not_null(con, table: str, columns: Iterable[str]) -> None:
    table = _validate_identifier(table)
    for col in columns:
        col = _validate_identifier(col)
        n = _scalar(con, f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL")
        assert n == 0, f"{table}.{col} has {n} NULL rows"


def assert_in_set(con, table: str, col: str, allowed: set) -> None:
    table = _validate_identifier(table)
    col = _validate_identifier(col)
    quoted = ", ".join(_quote_literal(v) for v in allowed)
    n = _scalar(
        con,
        f"SELECT COUNT(*) FROM {table} WHERE {col} NOT IN ({quoted})",
    )
    assert n == 0, f"{table}.{col}: {n} rows outside allowed set {allowed}"


def assert_range(con, table: str, col: str, lo=None, hi=None) -> None:
    table = _validate_identifier(table)
    col = _validate_identifier(col)
    conds = []
    if lo is not None:
        conds.append(f"{col} < {lo}")
    if hi is not None:
        conds.append(f"{col} > {hi}")
    if not conds:
        return
    where = " OR ".join(conds)
    n = _scalar(con, f"SELECT COUNT(*) FROM {table} WHERE {where}")
    assert n == 0, f"{table}.{col}: {n} rows out of range [{lo}, {hi}]"


def assert_fk(con, table: str, fk: str, ref_table: str, ref_col: str) -> None:
    table = _validate_identifier(table)
    fk = _validate_identifier(fk)
    ref_table = _validate_identifier(ref_table)
    ref_col = _validate_identifier(ref_col)
    n = _scalar(
        con,
        f"""
        SELECT COUNT(*)
        FROM {table} t
        LEFT JOIN {ref_table} r ON r.{ref_col} = t.{fk}
        WHERE t.{fk} IS NOT NULL AND r.{ref_col} IS NULL
        """,
    )
    assert n == 0, f"{table}.{fk} -> {ref_table}.{ref_col}: {n} orphan rows"


def assert_row_count_within(con, table: str, lo: int, hi: int) -> None:
    table = _validate_identifier(table)
    n = _scalar(con, f"SELECT COUNT(*) FROM {table}")
    assert lo <= n <= hi, f"{table} row count {n} outside expected [{lo}, {hi}]"


# --- pandas helpers (when working in-memory) --------------------------------

def df_assert_pk_unique(df, pk: str) -> None:
    assert df[pk].is_unique, (
        f"{pk} not unique: {len(df)} rows, {df[pk].nunique()} distinct"
    )


def df_assert_not_null(df, columns: Iterable[str]) -> None:
    for col in columns:
        n = int(df[col].isna().sum())
        assert n == 0, f"{col} has {n} NULL rows"


def df_assert_in_set(df, col: str, allowed: set) -> None:
    bad = ~df[col].isin(allowed)
    n = int(bad.sum())
    assert n == 0, f"{col}: {n} rows outside allowed set {allowed}"


def df_assert_range(df, col: str, lo=None, hi=None) -> None:
    bad = df[col].notna() & (
        ((df[col] < lo) if lo is not None else False)
        | ((df[col] > hi) if hi is not None else False)
    )
    n = int(bad.sum())
    assert n == 0, f"{col}: {n} rows out of range [{lo}, {hi}]"
