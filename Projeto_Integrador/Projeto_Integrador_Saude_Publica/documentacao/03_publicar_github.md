# Colocar o projeto e o dashboard no GitHub

Este roteiro publica os códigos **e** o dashboard estático. O arquivo inicial do site é `docs/index.html`.

## 1. Abrir no VS Code

1. Descompacte o ZIP do GitHub.
2. Abra a pasta `Projeto_Integrador_Saude_Publica` no VS Code.
3. Confira os arquivos, principalmente `README.md`, `codigo/` e `docs/`.
4. Para testar o painel, abra `docs/index.html` no navegador. O painel também funciona com Live Server.

## 2. Criar um repositório

No site do GitHub, crie um repositório vazio chamado `projeto-integrador-saude-publica`. No terminal do VS Code, dentro da pasta do projeto:

```bash
git init
git branch -M main
git add .
git status
git commit -m "Projeto integrador: ETL, analises e dashboard"
git remote add origin https://github.com/SEU-USUARIO/projeto-integrador-saude-publica.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário. Para atualizar depois: `git add .`, `git commit -m "Atualizacao do projeto"` e `git push`.

## 3. Deixar o dashboard acessível por um link

Depois de enviar os arquivos, no repositório do GitHub:

1. Abra **Settings > Pages**.
2. Em **Build and deployment**, escolha **Deploy from a branch**.
3. Selecione `main` e a pasta `/docs`; clique em **Save**.
4. Depois que a publicação terminar, o site terá um endereço semelhante a:
   `https://SEU-USUARIO.github.io/projeto-integrador-saude-publica/`
5. Cole esse link na seção Dashboard do README do repositório e compartilhe o link do repositório com o professor.

Documentação do GitHub: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Segurança e origem

- Não publicar `dados/00_original_privado/`: contém identificadores da base fornecida.
- Não publicar `documentacao/Enunciado_Professor.pdf` sem autorização.
- O `.gitignore` exclui esses itens e o banco/modelo binários.
- Os dados epidemiológicos simulados são marcados no próprio CSV e no painel.
- Revise as alterações com `git status` antes de publicar.

**Atenção:** GitHub Pages hospeda o dashboard HTML. O trabalho também cita **Google Looker Studio** e essa versão deve ser criada e compartilhada à parte se for exigida na correção.
