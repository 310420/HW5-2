#include <stdio.h>
#include <stdlib.h>

int recursiveMaximum(int num[], int u);
int u = 3;
int main()
{
	int i, ans, n;
	printf("��J�}�C���׬�3\n");


	int x[3];

	for (i = 0; i < 3; i++)
	{
		printf("��J��%d����:", i + 1);
		scanf("%d", &n);
		x[i] = n;
	}

	ans = recursiveMaximum(x, u);
	printf("�̤j�Ȭ�%d", ans);

	printf("\n");

	system("pause");
	return 0;
}

int recursiveMaximum(int num[], int u)
{


	if (u == 1)
		return num[0];

	if (recursiveMaximum(num, u - 1) < num[u - 1])
		return num[u - 1];
	else
		return recursiveMaximum(num, u - 1);
	recursiveMaximum(num, u - 1);

}