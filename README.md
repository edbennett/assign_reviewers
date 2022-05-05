# Simple reviewer assignment

Given CSV files containing submissions and reviewers (and the maximum number
of submissions they are willing to review), and the number of reviews per
submission.

## Strategy

Distribute submissions weighted by the number more submissions each reviewer is willing to
review, after disqualifying any reviewers already assigned to review a given submission.
Assign each submission one reviewer before moving on to assign second reviewers.

## Requirements

Requires Python 3.5+.

## Usage

~~~bash
usage: assign_reviewers.py [-h]
                           [--reviewer_id_column REVIEWER_ID_COLUMN]
                           [--max_reviews_column MAX_REVIEWS_COLUMN]
                           [--submission_id_column SUBMISSION_ID_COLUMN]
                           [--delimiter DELIMITER]
                           [--header_length HEADER_LENGTH]
                           [--seed SEED]
                           reviewers_file
                           submissions_file
                           reviews_per_submission
~~~

Required arguments:

* `reviewers_file`: a CSV file containing at least two columns, the identifier for
  the reviewer, and the maximum number of submissions that reviewer will review;
* `submissions_file`: a CSV file containing at least one column, the identifier for
  the submission;
* `reviews_per_submission`: the number of reviews each submission needs.

Optional arguments:
* `--reviewer_id_column`: the column in which the reviewer ID is, indexed from 0.
  Default is `0`.
* `--max_reviews_column`: the column in which the maximum number of reviewers for each
  reviewer is, indexed from 0. Default is `1`.
* `--submission_id_column`: the column in which the submission ID is, indexed from 0.
  Default is `0`.
* `--delimiter`: the delimiter used in the CSV files. Default is `,`.
* `--header_length`: the number of rows at the top of the file that give column
  headings rather than being data to be considered. Default is `0` (no header).
* `--seed`: the random seed passed (as a string) to `random.seed()`. This allows
  reproducible runs, even between versions of Python. Default is `None`; i.e.,
  seeding based on the current system time, which is not reproducible.

## Limitations

In very constrained cases there may be scenarios where the algorithm runs out of
eligible reviewers, even though in principle there are alternative assignments
that would have allowed all submissions to be reviewed. This is due to the naïvité
of the algorithm; while in principle enough random attempts could allow the solution
to be bruteforced, it's more likely that a better algorithm is needed.
