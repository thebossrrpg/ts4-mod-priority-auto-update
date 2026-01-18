# TS4 MOD AUTO‑CLASSIFIER — MODELO CANÔNICO

**Status:** CONGELADO 🔒  
**Alterações somente com justificativa excepcional.**

Este documento é a **fonte de verdade definitiva** do projeto **TS4 Mod Priority Auto Update**.  
Ele consolida o modelo mental, as regras de inferência e a taxonomia oficial.

Qualquer código, UI, automação ou integração **DEVE obedecer este documento**.  
Se houver divergência entre código e este arquivo, **o código está errado**.

---

## 1. Princípios Fundamentais

- O sistema é um **classificador categórico de domínio fechado**.
- Não existem eixos livres (número + letra).
- Não existem categorias fora da lista definida.
- A LLM **não decide prioridade** — apenas ajuda na leitura técnica.
- Incerteza **gera cautela**, nunca conforto.

---

## 2. Domínio Fechado de Categorias

Categorias válidas e **somente estas**:

### Prioridade 0 — Cinza (Cosmético Global)
- Override visual puro
- Zero lógica, zero script, zero impacto funcional

### Prioridade 1 — Vermelho (Core / Framework)
- Mods essenciais
- Quebram o jogo se ausentes ou quebrados

### Prioridade 2 — Amarelo (Sistemas Grandes / Overhauls)
- Sistemas amplos
- Impacto profundo, mas não core absoluto

### Prioridade 3 — Gameplay Ativo (Não Persistente)
- **3A** — Eventos & Festas
- **3B** — Feriados & Calendário
- **3C** — Família & Relações Pontuais
- **3D** — Skills, Hobbies & Carreiras Leves
- **3E** — Objetos Funcionais Específicos
- **3F** — Outros Gameplay Localizado (QoL com script)

### Prioridade 4 — Dados Persistentes (Identidade do Sim)
- **4A** — Aspirações
- **4B** — Traços & Personalidade (**sempre 4B, sem exceção**)
- **4C** — Storytelling de Cena
- **4D** — Marcos Narrativos (Milestones)

### Prioridade 5 — Regras Globais Voláteis
- **5A** — Filtros de Menu & Seleção
- **5B** — Utilitários de Gestão
- **5C** — Math Tuning
- **5D** — Fixes & Tweaks
- **5E** — Temas & Imersão Leve (*somente se puramente estético*)

❌ Combinações inválidas não existem (ex: 4E, 5F).

---

## 3. Equação Central de Inferência

```
Score = Remoção + Framework + Essencial
```

### 3.1 Remoção — Impacto ao remover
- 0   — puramente visual
- 1   — tuning / regra volátil
- 2   — comportamento localizado
- 3   — sistema grande
- 4   — core / quebra save ou outros mods

Intermediários permitidos: `0.5 / 1.5 / 2.5 / 3.5`

### 3.2 Framework
- 0   — não é dependência
- 0.5 — dependência indireta
- 1   — core / library

### 3.3 Essencial
- 0 — flavor / estético / nichado
- 1 — gameplay localizado / QoL
- 2 — gameplay grande / sistema relevante
- 3 — crítico / estrutural

Intermediários permitidos.

---

## 4. Score Contínuo e Arredondamento

- O score pode ser decimal.
- **Regra absoluta:** sempre arredondar PARA CIMA.

```
score_final = ceil(score_continuo)
```

Incerteza gera cautela.

---

## 5. Conversão Score → Prioridade

| Score final | Prioridade |
|------------|-----------|
| >= 7 | 1 (Vermelho) |
| 5–6 | 2 (Amarelo) |
| 3–4 | 3 (Verde) |
| 2 | 4 (Azul) |
| <= 1 | 0 (Cinza) |

---

## 6. Regras Absolutas de Exclusão

- **Prioridade 0 e 5E exigem mod PURAMENTE estético.**
- Se afeta jogabilidade, lógica, simulação ou inicialização → **nunca 0 ou 5**.
- Se o jogo não abre quando o mod quebra → **obrigatoriamente Prioridade 1**.

Teste humano canônico:
> "Se ele quebrar e eu não notar nada além de o detalhe ter sumido, então pode ser 0."

---

## 7. Classificação Temática

- É **discreta**.
- Uma e apenas uma categoria válida.
- Critério único:

> **Qual é a função principal do mod?**

- Efeitos colaterais **não mudam o tema**, mas **aumentam o score**.
- Ambiguidade real → **pedir validação humana**.

---

## 8. Subclassificação

- Subclassificação **NUNCA define prioridade**.
- Só organiza dentro de uma prioridade válida.
- Traços = **4B sempre**.

---

## 9. Contrato de Saída do App

Toda análise deve retornar:

- Existe no Notion? (sim/não)
- Classificação atual no Notion
- Classificação sugerida (com subclassificação)
- Divergência? (sim/não)
- Motivos da sugestão (se houver divergência)
- Aprovação explícita do usuário antes de escrever no Notion

---

## 10. Escrita no Notion

- `Priority` recebe **apenas o número**.
- Subclassificação vai para `Notes` (append‑only).
- Nunca sobrescrever decisão humana sem aprovação.

---

## 11. Regra Final

> **Este modelo está congelado.**  
> Alterações só são permitidas com justificativa excepcional documentada.

