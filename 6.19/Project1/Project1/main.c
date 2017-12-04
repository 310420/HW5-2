#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void shuffle(int wDeck[][6]);


int main(void)
{
	const int *suit[6] = { 1,2,3,4,5,6 };

	const int *face[6] ={ 1,2,3,4,5,6 };

	int deck[6][6] = { {2,3,4,5,6,7} ,{3,4,5,6,7,8},{4,5,6,7,8,9},
	                    {5,6,7,8,9,10},{6,7,8,9,10,11},{7,8,9,10,11,12} };

	srand(time(0));

	shuffle(deck);

	system("pause");
	return 0;
}



void shuffle(int wDeck[][6])
{
	int row, column, i;
    int D[11] = { 0 };

	for (i = 1; i <= 3600; i++)
	{
		row = rand() % 6;
	    column = rand() % 6;
		switch (wDeck[row][column])
		{
		case 2:
			D[0] = D[0] + 1;
			break;
		case 3:
			D[1] = D[1] + 1;
			break;
		case 4:
			D[2] = D[2] + 1;
			break;
		case 5:
			D[3] = D[3] + 1;
			break;
		case 6:
			D[4] = D[4] + 1;
			break;
		case 7:
			D[5] = D[5] + 1;
			break;
		case 8:
			D[6] = D[6] + 1;
			break;
		case 9:
			D[7] = D[7] + 1;
			break;
		case 10:
			D[8] = D[8] + 1;
			break;
		case 11:
			D[9] = D[9] + 1;
			break;
		case 12:
			D[10] = D[10] + 1;
			break;
		default:
			break;
		}

		
	}
	for ( i = 0; i <= 10; i++)
		printf("we have %d of the number %d\n", D[i], i + 2);	
}


