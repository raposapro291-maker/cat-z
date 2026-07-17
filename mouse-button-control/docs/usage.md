# Guia de Uso

## Interface Principal

A aplicação possui 7 abas principais:

### 1. Perfis

Gerenciar diferentes perfis de configuração.

**Funcionalidades:**
- Criar novos perfis
- Editar perfis existentes
- Duplicar perfis
- Deletar perfis
- Exportar/Importar perfis
- Ativar/Desativar perfis
- Visualizar detalhes do perfil

**Tipos de Perfis:**
- **Padrão**: Uso comum do computador
- **Jogos**: Otimizado para jogos
- **Trabalho**: Otimizado para produtividade
- **Personalizado**: Criado pelo usuário

### 2. Botões

Configurar ações para cada botão do mouse.

**Tipos de Ações:**
- **Nenhuma**: Desabilita o botão
- **Tecla**: Simula pressionamento de tecla
- **Comando**: Executa comando do terminal
- **Macro**: Executa macro personalizada
- **Controle de Mídia**: Play, pause, próxima, anterior, stop
- **Controle de Volume**: Aumentar, diminuir, mutar
- **Abrir Arquivo**: Abre arquivo específico
- **Abrir Pasta**: Abre pasta específica
- **Abrir Aplicativo**: Inicia aplicação
- **Desabilitar**: Bloqueia o botão

**Exemplo:**
1. Selecione o mouse
2. Selecione o botão (ex: Botão 5)
3. Selecione tipo de ação (ex: Comando)
4. Insira valor (ex: `firefox`)
5. Clique em Aplicar

### 3. Macros

Criar sequências complexas de ações.

**Como criar uma Macro:**

1. Clique em "Nova Macro"
2. Digite nome da macro
3. No editor visual, adicione ações:
   - Pressionar tecla
   - Soltar tecla
   - Esperar X ms
   - Executar comando
   - Clicar com mouse
4. Salve a macro

**Exemplo de Macro:**
```
1. Aguardar 100ms
2. Pressionar Ctrl+C (copiar)
3. Aguardar 50ms
4. Pressionar Ctrl+V (colar)
5. Aguardar 100ms
6. Pressionar Enter
```

### 4. Teclado

Configurar atalhos de teclado globais.

**Como configurar:**

1. Clique em "Nova Combinação"
2. Pressione as teclas desejadas (ex: Ctrl+Alt+X)
3. Selecione ação
4. Configure valor
5. Salve

**Atalhos Padrão:**
- `Ctrl+Alt+L`: Bloqueia mouse
- `Ctrl+Alt+U`: Desbloqueia mouse
- `Ctrl+Alt+P`: Alternar perfil

### 5. Automação

Configurar auto-troca de perfil por aplicação.

**Como configurar:**

1. Clique em "Adicionar Regra"
2. Selecione aplicação (ex: Steam)
3. Selecione perfil (ex: Jogos)
4. Salve

Quando você abrir o Steam, o perfil "Jogos" será ativado automaticamente.

**Exemplo de Regras:**
- Steam → Perfil Jogos
- Firefox → Perfil Padrão
- VS Code → Perfil Trabalho

### 6. Configurações

Personalizar comportamento da aplicação.

**Opções:**
- **Servidor de Display**: X11 ou Wayland (auto-detectado)
- **Iniciar com Sistema**: Sim/Não
- **Minimizar para Bandeja**: Sim/Não
- **Tema**: Claro/Escuro
- **Idioma**: Português/Inglês
- **Intervalo de Auto-save**: 60s
- **Habilitar Logs**: Sim/Não
- **Nível de Log**: DEBUG/INFO/WARNING/ERROR
- **Sensibilidade do Mouse**: 0.5 - 2.0
- **Auto-trocar Perfil**: Sim/Não

### 7. Logs

Visualizar histórico de ações executadas.

**Funcionalidades:**
- Visualizar logs em tempo real
- Filtrar por tipo de ação
- Filtrar por dispositivo
- Filtrar por perfil
- Exportar logs
- Limpar logs antigos
- Buscar em logs

## Recursos Avançados

### Camadas de Configuração

Cria perfis em camadas, permitindo sobrescrever configurações:

1. Base: Configuração padrão
2. Camada 1: Sobrescreve aspectos específicos
3. Camada 2: Sobrescreve mais aspectos

### Bloqueio de Botões

Desabilita botões específicos:

1. Vá para aba "Botões"
2. Selecione botão
3. Escolha "Desabilitar"
4. Aplique

### Repetição Automática

Repete ação ao manter botão pressionado:

1. Configure botão
2. Marque "Repetição Automática"
3. Defina intervalo (ms)
4. Aplique

### Clique Duplo Automático

Executa ação com clique duplo:

1. Configure botão
2. Marque "Clique Duplo"
3. Aplique

## Dicas e Truques

### Backup Automático

A aplicação faz backup automático a cada 60 segundos em:
```
~/.config/mouse-button-control/backups/
```

### Importar/Exportar Perfis

**Exportar:**
1. Selecione perfil
2. Clique em "Exportar"
3. Escolha local

**Importar:**
1. Clique em "Importar"
2. Selecione arquivo `.json`
3. Perfil será adicionado

### Editar Configuração Manualmente

As configurações estão em:
```
~/.config/mouse-button-control/config.db
```

Para editar diretamente:
```bash
sqlite3 ~/.config/mouse-button-control/config.db
```

## Troubleshooting

### Mouse não responde

1. Verifique se aplicação está rodando
2. Verifique se perfil está ativo
3. Consulte logs em "Logs"
4. Reinicie aplicação

### Macro não funciona

1. Verifique sintaxe da macro
2. Teste cada ação isoladamente
3. Ajuste delays entre ações
4. Consulte logs

### Perfil não troca automaticamente

1. Verifique se "Auto-trocar Perfil" está habilitado
2. Verifique se regra está correta
3. Verifique nome do aplicativo
4. Consulte logs

## Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl+S` | Salvar |
| `Ctrl+Z` | Desfazer |
| `Ctrl+Y` | Refazer |
| `Ctrl+Q` | Sair |
| `F1` | Ajuda |
| `F5` | Atualizar |

