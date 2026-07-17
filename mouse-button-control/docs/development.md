# Desenvolvimento

## Setup de Desenvolvimento

### Clone o repositório

```bash
git clone https://github.com/raposapro291-maker/cat-z.git
cd cat-z/mouse-button-control
```

### Crie um ambiente virtual

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### Instale dependências de desenvolvimento

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

## Estrutura do Projeto

```
mouse-button-control/
├── mouse_button_control/
│   ├── config/          # Gerenciamento de configuração
│   ├── device/          # Detecção e gerenciamento de dispositivos
│   ├── macro/           # Engine de macros
│   ├── automation/       # Automação de perfis
│   ├── system/          # Integração com sistema
│   ├── ui/              # Interface gráfica
│   ├── utils/           # Utilitários
│   ├── i18n/            # Internacionalização
│   └── main.py          # Ponto de entrada
├── tests/               # Testes automatizados
├── docs/                # Documentação
├── requirements.txt     # Dependências
├── setup.py            # Setup do projeto
└── README.md           # Readme principal
```

## Convenções de Código

### Estilo

Usamos **Black** para formatação:

```bash
black mouse_button_control/
```

### Linting

Usamos **Flake8** para linting:

```bash
flake8 mouse_button_control/
```

### Type Hints

Usamos **type hints** em todas as funções:

```python
def execute_action(self, action_type: str, action_value: str) -> bool:
    """Execute an action."""
    pass
```

### Documentação

Use docstrings em todos os módulos, classes e funções:

```python
def my_function(param1: str) -> int:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
    
    Returns:
        Description of return value
    """
    pass
```

## Testes

### Rodar todos os testes

```bash
pytest
```

### Rodar com cobertura

```bash
pytest --cov=mouse_button_control --cov-report=html
```

### Escrever novo teste

```python
# tests/test_action_executor.py
import pytest
from mouse_button_control.macro.action_executor import ActionExecutor

class TestActionExecutor:
    def setup_method(self):
        self.executor = ActionExecutor()
    
    def test_execute_key_action(self):
        assert self.executor.execute_action("key", "a") == True
    
    def test_execute_command(self):
        assert self.executor.execute_action("command", "echo test") == True
```

## Adicionando Novas Funcionalidades

### 1. Crie um branch

```bash
git checkout -b feature/minha-funcionalidade
```

### 2. Implemente a funcionalidade

```python
# Adicione código em mouse_button_control/
# Mantenha a estrutura modular
```

### 3. Escreva testes

```bash
# Adicione testes em tests/
pytest
```

### 4. Format e lint

```bash
black mouse_button_control/
flake8 mouse_button_control/
mypy mouse_button_control/
```

### 5. Faça commit

```bash
git add .
git commit -m "feat: descrição da funcionalidade"
```

### 6. Push e crie Pull Request

```bash
git push origin feature/minha-funcionalidade
```

## Debugging

### Logs

Verifique os logs em:
```
~/.config/mouse-button-control/logs/
```

### Print Debug

Use o logger para debug:

```python
from utils.logger import Logger

logger = Logger.get_logger()
logger.debug("Variável x:", x)
logger.info("Ação executada")
logger.warning("Aviso")
logger.error("Erro encontrado")
```

### Executar com Debug

```bash
python -m mouse_button_control.main --debug
```

## Performance

### Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Seu código aqui

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

## Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Código de Conduta

- Seja respeitoso
- Teste seu código
- Documente suas mudanças
- Siga as convenções

## Licença

MIT License - Veja LICENSE
