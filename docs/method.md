# Method and limitations

1. Read UTF-8 input (an optional UTF-8 BOM is accepted).
2. Apply Unicode case folding and normalize curly apostrophes.
3. Extract letter sequences, including internal apostrophes.
4. Count all words with `collections.Counter`.
5. Sort by descending frequency, then alphabetically for ties.
6. Save a JSON record; combine records into an HTML report.

## What is a word?

`Git git` produces two occurrences of `git`. `Код код` produces two
occurrences of `код`. Numbers and underscores separate words.
The tokenizer is educational: it does not perform linguistic lemmatization.

## Raw Markdown, not rendered prose

URLs, code snippets, image descriptions and Markdown metadata are included.
Common words such as `the` are not filtered. Do not interpret this analysis
as a reading-quality score or a semantic comparison between frameworks.

## Repeatability

The source snapshots are committed with SHA-256 checksums and upstream commit
references. The analyzer performs no downloads. Identical input bytes and
parameters under the same Python environment produce identical JSON.

The report includes every `*.json` in its input folder. Use a dedicated result
folder for each dataset; old results remain until deliberately removed.
The report's total counts word occurrences across files, not unique vocabulary
across the whole collection. Each bar chart has its own scale.

## Errors

Missing files, invalid UTF-8 and non-positive `--top` values produce a nonzero
exit code. A report with no input JSON files is an error. An empty document is
valid and has zero words.
