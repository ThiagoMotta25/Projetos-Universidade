#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void menu() 
{
    printf("                   ------------------ Terminal da loja informatica --------------------         ");
}
////////////////////////Definicao dos tipos/////////////////////////////
typedef struct produtos
{
    char nome[200];
    char marca[200];
    int id;
    float preco;
    int numero_stock;
    struct produtos* next;
} Um_produto;



//////////////////funcoes ou prototipos das funcoes///////////////////////////////

//////////////////////Inserir um novo produto na list/////////////////////////
void inserir_produto(Um_produto** lista)
{
    Um_produto* aux = (Um_produto*)malloc(sizeof(Um_produto));


    printf("Nome: ");                     
    scanf("%s", &aux->nome);

    printf("Marca: ");                     
    scanf("%s", &aux->marca);

    printf("ID: ");
    scanf("%d", &aux->id);

    printf("preco:  ");
    scanf("%f", &aux->preco);

    aux->numero_stock = 0;

    aux->next = *lista;
    *lista = aux;
}

////////////////////listar todos os produtos//////////////////////////////
void listar(Um_produto* lista)
{
    printf("********************************************************************************\n");
    Um_produto* aux = lista;
    aux = lista; // aux fica a apontar para o inico da lista
    while (aux != NULL)
    {
        printf("Nome:%s  Marca:%s  ID:%d preco:%f Numero strock:%d\n", aux->nome, aux->marca, aux->id, aux->preco, aux->numero_stock);
        aux = aux->next;
    }
    printf("******************************************************************************\n");
}



////////////Editar a informacao de um produto(Nome,Marca,Id,preco)/////////////////
int editar(Um_produto** lista)
{

    int id;
    Um_produto* aux = (*lista);
    printf("qual ID do produto para editar?: ");
    scanf("%d", &id);
    if (!aux)
        printf("O produto nao existe...");// encerra se não houver item na lista
    while(aux!=NULL){
        if (aux->id == id) {
            printf("--------Novo dados do produto-------\n");
            printf("Nome: ");
            scanf("%s", &aux->nome);

            printf("Marca: ");
            scanf("%s", &aux->marca);

            printf("ID: ");
            scanf("%d", &aux->id);

            printf("preco:  ");
            scanf("%f", &aux->preco);
            printf("------------------------------------\n");
        }
        aux = aux->next;
    }
    return 1;
    
}
//////////////////////alterar numeno stock////////////////////
int editar_stock(Um_produto** lista) 
{
    printf("ID do produto?: \n");
    int id;
    scanf("%d", &id);
    Um_produto* aux = (*lista);
    while (aux != NULL){
        if (aux->id == id) {
            printf("numero do stock:  ");
            scanf("%d", &aux->numero_stock);
        }
        aux = aux->next;
    }
    return 1;
}
//////////////////////alterar preco////////////////////
int editar_preco(Um_produto** lista) 
{
    printf("ID do produto?: \n");
    int id;
    scanf("%d", &id);
    Um_produto* aux = (*lista);
    while (aux != NULL){
        if (aux->id == id) {
            printf("preco:  ");
            scanf("%f", &aux->preco);
        }
        aux = aux->next;
    }
    return 1;
}
////////////Remover um produto da lista///////////


int remover_item(Um_produto** lista)
{
    Um_produto* aux = (*lista);
    int id;
    printf("ID para remover :");
    scanf("%d", &id);
    if (!aux)
       printf("O produto nao existe..."); // encerra se não houver item na lista
    
    if (aux->id == id) // verifica se posição == 0
    {
        (*lista) = (*lista)->next;
        free(aux); // limpa a memória

        return 1;
    }

    Um_produto* ant;
    while (aux) // verifica se aux não chegou ao fim e percorre a posição
    {
        ant = aux; // ant guarda valor da remoção
        aux = aux->next;
        if (aux && aux->id == id) // verifica o id 
        {
            ant->next = aux->next;
            free(aux);
            return 1;
        }
    }
    return 0;
}

//////////////////////Indicar o ID de produto inscritos na lista.////////////////////////////
void imprimir_produto_com_id(Um_produto* lista)
{
    Um_produto* aux = lista;
    int ID, encontrou = 0;
    printf("ID?: ");
    scanf("%d", &ID);
    printf("teste \n");
    while (aux != NULL && encontrou == 0) {
        printf("teste2 \n");
        if (ID == aux->id) {
            encontrou = 1;
            printf("*******************************\n");
            printf("ID: %d\n", aux->id);
            printf("NOME: %s\n", aux->nome);
            printf("Marca: %s\n", aux->marca);
            printf("Preco: %f\n", aux->preco);
            printf("*******************************\n");
        }
        aux = aux->next;
    }
}

/////////////////////main//////////////////////
int main()
{
    int escolhe;
    Um_produto* lista = NULL;
    do
    {

        printf("                  MENU                     \n");
        printf("1-Inserir um novo produto na lista\n");
        printf("2-Editar a informacao de um produto(Nome,Marca,Id,preco)\n");
        printf("3-Consulta o ID de produto inscritos na lista.\n");
        printf("4-Remover um produto da lista\n");
        printf("5-listar todos os produtos\n");
        printf("6-Editar numero de stock\n");
        printf("7-Editar preco de um produto\n");

        printf("0-sair\n");
        scanf("%d", &escolhe);

        switch (escolhe)
        {
        case 1:
            inserir_produto(&lista);
            break;
        case 2:
            editar(&lista);
            break;
        case 4:
            remover_item(&lista);
            break;
        case 5:
            listar(lista);
            break;
        case 3:
            imprimir_produto_com_id(lista);
            break;
        case 6:
            editar_stock(&lista);
            break;
        case 7:
            editar_preco(&lista);
            break;
        case 0:
            printf("END");
        default:
            printf("\ninvalida");
        }
    } while (escolhe != 0);

    // liberta o espaco alocado para al lista////////
    free(lista);

    return 0;
}


