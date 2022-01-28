int main()
{
    int a = 10;
    int b = 100;
    int r;

    while(b != 0)
    {
        r = a % b;
        a = b;
        b = r;
    }
    printf("NWD: %d\n", a);
    return 0;
}