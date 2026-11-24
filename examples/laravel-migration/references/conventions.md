# Migration conventions (example)

Adapt these to your project; they illustrate what belongs in a reference file.

## Naming
- `create_<table>_table`, `add_<column>_to_<table>_table`, `drop_<column>_from_<table>_table`.
- Table names: plural snake_case. Pivot tables: singular names in alphabetical order (`post_tag`).

## Columns
- Primary keys: `id()`. Timestamps: `timestamps()`. Soft deletes only when the model uses them.
- Money: `decimal(12, 2)`, never float.
- Booleans: `boolean()` with an explicit `default()`.
- New non-null columns on existing tables need a default or must be added nullable first.

## Indexes and keys
- Index every foreign key column and every column used in frequent `where` clauses.
- Foreign keys: `foreignId('x_id')->constrained()` with an explicit `cascadeOnDelete()` or `restrictOnDelete()`.

## Safety
- `down()` must reverse `up()` exactly (drop foreign keys before columns).
- Never edit a migration that has already been deployed; add a new one.
