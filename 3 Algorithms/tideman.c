#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;
int voter_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
int getCycleLength(int index, int lCounter, int mCounter);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        // i is preffered to all those that follow
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int currentCandidateIndex = 0; currentCandidateIndex < candidate_count; currentCandidateIndex++)
    {
        for (int otherCandidateIndex = 0; otherCandidateIndex < candidate_count; otherCandidateIndex++)
        {
            // skip checking candidate against themself
            if (currentCandidateIndex != otherCandidateIndex)
            {
                // add if preference is a majority
                if (preferences[currentCandidateIndex][otherCandidateIndex] > preferences[otherCandidateIndex][currentCandidateIndex])
                {
                    pairs[pair_count].winner = currentCandidateIndex;
                    pairs[pair_count].loser = otherCandidateIndex;
                    pair_count++;
                }
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int lengthToCheck = pair_count;

    while (lengthToCheck > 1)
    {
        for (int i = 0; i < lengthToCheck; i++)
        {
            pair tempHolder;
            pair focusPair = pairs[i];
            pair comparisonPair = pairs[i + 1];

            // get pairs preference weight
            int focusPairWinnerVotes = preferences[focusPair.winner][focusPair.loser];
            int comparisonPairWinnerVotes = preferences[comparisonPair.winner][comparisonPair.loser];

            // using a bubble sort as the max lenght of 9 candidates does not require a more complex solution
            if (focusPairWinnerVotes < comparisonPairWinnerVotes)
            {
                // use a temp to switch items in the list
                tempHolder = focusPair;
                focusPair = comparisonPair;
                comparisonPair = tempHolder;

                // update the pairs list
                pairs[i] = focusPair;
                pairs[i + 1] = comparisonPair;
            }
        }

        // end of list now sorted by default
        lengthToCheck--;
    }

    return;
}

void lock_pairs(void)
{
    // initialisation of loops for recursive function
    int loopCounter = 0;
    int matchesCounter = 0;

    for (int pairIndex = 0; pairIndex < pair_count; pairIndex++)
    {
        pair currentPair = pairs[pairIndex];
        locked[currentPair.winner][currentPair.loser] = true;

        // check length of preferences cycle
        int cycleLength = getCycleLength(currentPair.winner, loopCounter, matchesCounter);

        // If cycle of preferences == candidate_count, reverse the recent, weakest lock
        if (cycleLength == candidate_count)
        {
            locked[currentPair.winner][currentPair.loser] = false;
        }
    }

    return;
}

// Print the winner of the election
void print_winner(void)
{
    // if all J's empty, J is the winner as no candidate has a lock over them
    for (int j = 0; j < candidate_count; j++)
    {
        bool allFalse = true;

        for (int i = 0; i < candidate_count; i++)
        {
            if (i != j)
            {
                if (locked[i][j] == true)
                {
                    allFalse = false;
                    break;
                }
            }
        }

        if (allFalse)
        {
            printf("%s\n",candidates[j]);
            break;
        }
    }

    return;
}

// detect if there is a cycle in preferences, if so, discard weakest lock
int getCycleLength(int index, int lCounter, int mCounter)
{
    // The loser of the 'current pair' - used to look if it is locked over another candidate
    int currentIndex = index;

    int loopCounter = lCounter;
    int matchCounter = mCounter;

    loopCounter++;

    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[currentIndex][i] == true)
        {
            matchCounter++;

            if (loopCounter == candidate_count)
            {
                return matchCounter;
            }
            else
            {
                // recursively call this function until called candidate_count times, or chain is broken
               return getCycleLength(i, loopCounter, matchCounter);
            }
        }
    }

    // chain broken, exit
    return matchCounter;
}
