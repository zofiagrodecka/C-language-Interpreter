float global = 5.0;

int main(){
    int a;
    a = 1;
    int i = 3;
    float f = 1.2 / global;
    f *= 5.;
    global++;
    //printf("global: %f, i: %f\n", global, i, a);
    if( i > 5){
        while(i > 0){
            printf("%d\n", i);
            i-= 2;
        }
        //break;
    }
    else{
        while(i > 0){
            if(i == 2){
                break;
            }
            printf("%d\n", i);
            i--;
        }
    }

    for( int j = 0; j<5; j += 2 ){
        if(j == 2){
            continue;
        }
        printf("j= %d\n", j);
    }

    int N = 5;
    int tab[N];
    for(int k=0; k<N; k++){
        tab[k] = k;
        printf("%d ", tab[k]);
    }
    printf("\n");

    string str = "Ala";
    int aaaaab = 10;
    aaaaab /= 10;

    char c = '!';
    bool always_true = true;
    printf("Hello World!\n");
    printf("Hej %s\n", str);
    //printf("Wartosc a to: %f\n", a);
    //printf("Wypisz na ekran %q\n", a);
    return 0;
    printf("Tego nie powinien wypisac\n");
}