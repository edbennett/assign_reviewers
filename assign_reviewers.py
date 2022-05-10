from csv import reader
from random import choice, seed


def get_args():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser()
    parser.add_argument('reviewers_file', type=FileType('r'))
    parser.add_argument('submissions_file', type=FileType('r'))
    parser.add_argument('reviews_per_submission', type=int)
    parser.add_argument('--reviewer_id_column', type=int, default=0)
    parser.add_argument('--max_reviews_column', type=int, default=1)
    parser.add_argument('--submission_id_column', type=int, default=0)
    parser.add_argument('--submitter_id_column', type=int, default=None)
    parser.add_argument('--delimiter', default=',')
    parser.add_argument('--header_length', type=int, default=0)
    parser.add_argument('--seed', default=None)
    return parser.parse_args()


def get_reviewers(
        reviewers_file, id_column, max_reviews_column, delimiter, header_length
):
    reviewer_max_subs = {}
    for idx, row in enumerate(reader(reviewers_file, delimiter=delimiter)):
        if idx < header_length:
            continue
        reviewer_max_subs[row[id_column]] = int(row[max_reviews_column])

    return reviewer_max_subs


def get_submissions(submissions_file, id_column, delimiter, header_length,
                    submitter_column=None):
    submissions = {}
    for idx, row in enumerate(reader(submissions_file, delimiter=delimiter)):
        if idx < header_length:
            continue
        submissions[row[id_column]] = (row[submitter_column]
                                       if submitter_column else None)
    return submissions


def get_eligible_reviewers(
        submission, submitter, reviewer_max_subs, reviewer_subs
):
    eligible_reviewers = [
        reviewer
        for reviewer in reviewer_subs
        for _ in range(reviewer_max_subs[reviewer] - len(reviewer_subs[reviewer]))
        if (submission not in reviewer_subs[reviewer])
        and (reviewer != submitter)
    ]
    if not eligible_reviewers:
        raise RuntimeError(
            'We ran out of reviewers. Possibly bad luck, or possibly we need a '
            'better algorithm. Maybe try again?'
        )
    return eligible_reviewers


def assign_reviewers(submissions, reviewer_max_subs, reviews_per_submission):
    reviewer_subs = {reviewer: [] for reviewer in reviewer_max_subs}

    for _ in range(reviews_per_submission):
        for submission, submitter in submissions.items():
            eligible_reviewers = get_eligible_reviewers(
                submission, submitter, reviewer_max_subs, reviewer_subs
            )
            reviewer_subs[choice(eligible_reviewers)].append(submission)

    return reviewer_subs


def check_viability(submissions, reviewer_max_subs, reviews_per_submission):
    if (
            len(submissions) * reviews_per_submission
            > sum(reviewer_max_subs.values())
    ):
        raise ValueError('Not enough reviewers!')

    if len(set(submissions)) != len(submissions):
        raise ValueError('Duplicate submission IDs')


def print_subs_per_reviewer(reviewer_subs):
    print("Submission assignments per reviewer:")
    for reviewer, this_reviewer_subs in reviewer_subs.items():
        print(f'{reviewer}: {", ".join(map(str, this_reviewer_subs))}')


def print_reviewers_per_sub(reviewer_subs):
    submissions = set([sub for subs in reviewer_subs.values() for sub in subs])
    print("Reviewer assignments per submission:")
    for submission in submissions:
        sub_reviewers = [
            reviewer
            for reviewer, this_reviewer_subs in reviewer_subs.items()
            if submission in this_reviewer_subs
        ]
        print(f'{submission}: {", ".join(sub_reviewers)}')


def main():
    args = get_args()
    seed(args.seed)

    reviewer_max_subs = get_reviewers(
        args.reviewers_file, args.reviewer_id_column, args.max_reviews_column,
        args.delimiter, args.header_length
    )
    submissions = get_submissions(
        args.submissions_file, args.submission_id_column,
        args.delimiter, args.header_length,
        submitter_column=args.submitter_id_column
    )
    check_viability(
        submissions,
        reviewer_max_subs,
        args.reviews_per_submission
    )

    reviewer_subs = assign_reviewers(
        submissions,
        reviewer_max_subs,
        args.reviews_per_submission
    )

    print_subs_per_reviewer(reviewer_subs)
    print()
    print_reviewers_per_sub(reviewer_subs)


if __name__ == '__main__':
    main()
