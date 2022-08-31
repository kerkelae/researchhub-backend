ALL = "ALL"  # ALL includes paper and posts
DISCUSSION = "DISCUSSION"
ELN = "ELN"
HYPOTHESIS = "HYPOTHESIS"
NOTE = "NOTE"
PAPER = "PAPER"
POSTS = "POSTS"  # POSTS include discussion and eln
QUESTION = "QUESTION"
BOUNTY = "BOUNTY"

DOCUMENT_TYPES = (
    (DISCUSSION, DISCUSSION),
    (ELN, ELN),
    (HYPOTHESIS, HYPOTHESIS),
    (NOTE, NOTE),
    (PAPER, PAPER),
    (QUESTION, QUESTION),
)

RESEARCHHUB_POST_DOCUMENT_TYPES = [DISCUSSION, ELN, POSTS, QUESTION]

FILTER_ALL = ALL
FILTER_ANSWERED = "FILTER_ANSWERED"
FILTER_AUTHOR_CLAIMED = "FILTER_AUTHOR_CLAIMED"
FILTER_BOUNTY_CLOSED = "FILTER_BOUNTY_CLOSED"
FILTER_BOUNTY_EXPIRED = "FILTER_BOUNTY_EXPIRED"
FILTER_BOUNTY_OPEN = "FILTER_BOUNTY_OPEN"
FILTER_HAS_BOUNTY = "FILTER_HAS_BOUNTY"
FILTER_OPEN_ACCESS = "FILTER_OPEN_ACCESS"
FILTER_PEER_REVIEWED = "FILTER_PEER_REVIEWED"
SORT_BOUNTY_EXPIRATION_DATE = "SORT_BOUNTY_EXPIRATION_DATE"
SORT_BOUNTY_TOTAL_AMOUNT = "SORT_BOUNTY_TOTAL_AMOUNT"
SORT_DISCUSSED = "SORT_DISCUSSED"
SORT_UPVOTED = "SORT_UPVOTED"
