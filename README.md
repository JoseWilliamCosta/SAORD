# SAORD

**Sistema de Armazenamento e Organização de Documentos**

---

## 🚀 Comandos básicos para subir o projeto no GitHub

### Inicialização do repositório

```
git init
```

### Adicionar arquivos ao controle de versão

```
git add .
```

### Criar o primeiro commit

```
git commit -m "Primeiro commit"
```

### Conectar o projeto ao repositório remoto

```
git remote add origin https://github.com/JoseWilliamCosta/SAORD
```

### Conferir se o repositório remoto foi adicionado

```
git remote -v
```

---

## 🌿 Trabalho com branches

As **branches** serão criadas de acordo com as tarefas do projeto.

### Convenção adotada:

* `main` → versão estável do projeto
* `front` → desenvolvimento do front-end
* `back` → desenvolvimento do back-end

Outras branches podem ser criadas conforme a necessidade.

---

## 🔧 Fluxo de trabalho com branches (exemplo: Front-end)

### Atualizar as branches do GitHub no repositório local

```
git pull
```

### Verificar em qual branch você está

```
git branch
```

> A branch atual aparece com um `*`.

---

### Mudar para a branch `front`

```
git checkout front
```

ou

```
git switch front
```

---

### Atualizar a branch atual com a `main`

```
git pull origin main --rebase
```

---

### Após realizar as modificações

```
git add .
git commit -m "Descrição das alterações"
```

---

### Enviar a branch para o GitHub

```
git push
```
---
## Divisão do Trabalho:
* Documentação: Warley
* Front End: Pedro Henrique
* Back End: Arthu
* Slide: Fernanda
* Correções e ajuda em geral(Linder): William
---

## ✅ Observações finais

* Sempre mantenha sua branch atualizada com a `main`
* Evite commits diretamente na `main`
* Utilize mensagens de commit claras e objetivas

