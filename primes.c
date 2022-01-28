int main(){
    bool tab[1000];
    int n = 13;  // maksymalna liczba, do ktorej są wypisywane liczby pierwsze
    int wielokr;

    for(int i=2; i<=n; i++){
        tab[i] = true;
    }

    for(int i=2; i<=n; i++){
        if(tab[i] == true){
            wielokr = i*i;
            while(wielokr <= n){
                tab[wielokr] = false;
                wielokr += i;
            }
        }
    }

    for(int i=2; i<=n; i++){
        if(tab[i] == true){
            printf("%d\n", i);
        }
    }

    return 0;
}