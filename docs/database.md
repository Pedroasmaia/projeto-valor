# Estrutura da Base de Dados:

~~~mermaid
classDiagram
    class User {
        +id_valor : int
        +id_discord : string
        +name : string
        +qtd_perguntar : int
        +create_at : datetime
    }

    class Daily {
        +id_daily : int
        +user_id : int
        +daily_text : string
        +created_at : datetime
    }

    User "1" --> "many" Daily : escreve

~~~