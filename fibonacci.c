int main(){
    int a = 0;
    int b = 1;
    int c = 2;
    int n = 20;
    printf("%d\n%d\n", a, b);
    while(c < n){
        a = a + b;
        printf("%d\n", a);
        b = b + a;
        printf("%d\n", b);
        c += 2;
    }

    return 0;
}