from random import choice

import pandas as pd


reviewers = pd.read_csv('test_data/test-reviewers.csv')
submissions = pd.read_csv('test_data/test-submissions.csv')

reviews_per_submission = 3


if len(submissions) * reviews_per_submission > reviewers['Maximum number of submissions willing to review'].sum():
    raise ValueError('Not enough reviewers!')
    
if len(set(submissions['Submission Id'])) != len(submissions):
    raise ValueError('Duplicate submission IDs')


reviewer_max_subs = dict(zip(reviewers.Username, reviewers['Maximum number of submissions willing to review']))
reviewer_subs = {reviewer: [] for reviewer in reviewer_max_subs}

for _ in range(reviews_per_submission):
    for submission in submissions['Submission Id']:
        eligible_reviewers = [
            reviewer
            for reviewer in reviewer_subs
            for _ in range(reviewer_max_subs[reviewer] - len(reviewer_subs[reviewer]))
            if submission not in reviewer_subs[reviewer]
        ]
        if not eligible_reviewers:
            raise RuntimeError('We ran out of reviewers. Possibly bad luck, or possibly we need a better algorithm. Maybe try again?')
        reviewer_subs[choice(eligible_reviewers)].append(submission)

print("Submission assignments per reviewer:")
for reviewer, this_reviewer_subs in reviewer_subs.items():
    print(f'{reviewer}: {", ".join(map(str, this_reviewer_subs))}')

print()
print("Reviewer assignments per submission:")
for submission in submissions['Submission Id']:
    sub_reviewers = [
        reviewer
        for reviewer, this_reviewer_subs in reviewer_subs.items()
        if submission in this_reviewer_subs
    ]
    print(f'{submission}: {", ".join(sub_reviewers)}')
