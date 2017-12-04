#include <stdio.h>
#include <stdlib.h>

void printStringBackward(char *str, int i) {
	if (str[i] != '\0') {
		printStringBackward(str, i + 1);
		printf("%c", str[i]);
	}
}

int main(void) {
	char str[60];
	printf("½Ð¿é¤J¦r¦ê :");
	gets(str);
	printStringBackward(str, 0);
	printf("\n");
	system("pause");
	return 0;
}