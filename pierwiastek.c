int main(){
    int n = 25;
    int indeks = 1;
    int wyraz = 1;
    int suma = 1;

    while(suma < n){
        wyraz += 2;
        suma += wyraz;
        indeks++;
    }

    if(suma > n){
        indeks--;
    }

    printf("%d\n", indeks);

    return 0;
}