---
title: sl4_Malthus
deploy: true
title_custom: true
tags: [slides/final]
created: 2023-02-06T21:13:32.340Z
modified: 2025-01-25T19:17:05.687Z
marp: true
---

<!--
theme: gaia 
paginate: true
footer: Eco 331
style: |
  section {font-size: 26px;}
-->


<!-- footer: "" -->


![bg right w:600](attachments/photo_popn.png)
### ECO 331
## Economic History

```
MALTHUS, POPULATION, HUMAN CAPITAL 
```
Jonathan Conning
Spring 2026
<br></br>

---
### Readings

<br></br>
- OG 2 "Lost in Stagnation" 27-41
- OG 3 "The Storm Beneath the Surface", 43-55.

- (optional:  KR 5 Fewer babies?)

Student presentation:
- Nunn, Nathan, and Nancy Qian. 2011. “The Potato’s Contribution to Population and Urbanization: Evidence from a Historical Experiment.” _The Quarterly Journal of Economics_ 126 (2): 593–650. ([PDF](https://drive.google.com/file/d/12EekL6XUzBIVkm4TMWyZndTCTvR5xkXI/view?usp=sharing))

---

## Demography in the pre-industrial world
- Life expectancy in Roman Egypt ~27-28 years (Harper, 2017)
    - LE in poorest countries today generally higher than pre-industrial past. 
- Infant mortality was high (Harper, 2017)
     - 30% of babies died \<1 yr in Roman world
- Life expectancy low even in richest parts of the world
  - In 1700 England it was 38 years at birth (considerably higher than France, or Roman Empire)
  - Queen Anne (rule 1702-1714): 17 pregnancies, 4 live births, no child survived past 10.   She died at 49.

![bg right:30% w:300](attachments/gr_queen_anne.png)

---
### Life Expectancy

[link](https://www.gapminder.org/tools/#$chart-type=bubbles&url=v1)

![bg center w:900](attachments/gr_gapminderlife.png)

---

<!-- footer: "" -->
![bg center:50%](attachments/og_epochs.png)




---
### Malthus Model

- $y$ income per capita
- TOP:
  - $b(y) \uparrow$ with $y$
  - $d(y) \downarrow$ with $y$
  - $b(y)>d(y) \rightarrow pop \uparrow$ 
- BOTTOM: 
  - $y \downarrow$ as pop $N \uparrow$
  (diminishing returns)

- IMPLICATION:
  - Always return to steady state: 
  - pop $N$ and income $y^*$
![bg right:60% w:700](attachments/Clark_malthus1.png)


---
#### Effect of lower birth date
![bg right:60% w:650](attachments/gc_malthus_br.png)

- Malthus' "preventative check"
- Efforts lower birth rate for any given $y$
- Examples
  - delay age of marriage
  - birth control

- At initial $y_1^*$ deaths exceed births
  - popn falls $N_1^*$ to $N_0^*$
  - income rises $y_1^*$ to $y_0^*$
- New steady state.

---

<!--
[geogebra app](https://www.geogebra.org/classic/gerp8eh6)  (draft, will be improved)
-->
### Explicit model (optional)

A simple system of differential equations determine population $N$ and total resources $Y$ (and hence $y=Y/N$) at each time instant $t$.
$$
\begin{align*}
\frac{dN}{dt} &= N(b(r) - d(r)) \\
\frac{dY}{dt} &= g - cN
\end{align*}
$$

- $y = \frac{Y}{N}$ (per capita resources)
- $b(y) = b_0y$ (birth rate increases linearly with resources)
- $d(y) = d_0e^{-\alpha y}$ (death rate decreases exponentially with resources)
 
- $g$ : resource growth rate
- $c$ : resource consumption rate per individual

---

#### Effect of raised death rate
(from 1 to 0 in the diagram)

![bg right:60% w:650](attachments/gc_malthus_dr.png)

- e.g. epidemic
- At initial $y_1^*$, deaths now exceed births
    - popn falls $N_1^*$ to $N_0^*$
    - income rises $y_1^*$ to $y_0^*$
- New steady state.



---
#### Effect of isolated Technological advance

![bg right:60% w:650](attachments/gc_malthus_tech.png)

- Starting from $(y^*, N_0^*)$
- bottom line shifts out (higher $y$ at any given $N$)
- Births now exceed Deaths
  - popn rises to $N_1^*$
  - income returns to $y*$

---
### Malthusian Dynamics (simulation) [colab notebook link](https://drive.google.com/file/d/1FH014dDalwQ0SADaOWhXjpK20epCsgyP/view?usp=sharing)
![bg center w:1200](attachments/Pasted%20image%2020250214103537.png)




---
#### Improvement in Technology in Malthusian World

![bg center w:700](attachments/Malthus2.jpg)


---
## Earlier Onset of Agriculture

- Tech advance $\rightarrow$
- Popn $\rightarrow$  tech advance
  - more people, diversity, specialization, human capital.

- Earlier onset $\rightarrow$ better technology
  + disease immunity, soldiers, etc
  + Not higher incomes per capita
+ Absorb, conquer, and/or exterminate/displace other societies  


---

Galor, p3:
![bg center w:900](attachments/ogq_compared.png)

---

#### Pop Growth in Europe before 1800

- High birth rate 
- High mortality
- Slow pop growth before 1800
- Table shows implied number of surviving children per woman:
![bg right w:650](attachments/clark_2_1.png)


---

![bg center w:900](attachments/og_years_pop.png)


---

![bg center w:900](attachments/og_land_pop.png)


---

![bg center w:950](attachments/og_land_gdpcap.png)

---


<iframe width="700" height="394" src="https://www.youtube.com/embed/yLGSDtCiswA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

[Population through the ages video](https://www.youtube.com/embed/yLGSDtCiswA)


---
#### Steady state need not mean minimum subsistence
###### Why are incomes in Malawi today below those of England 1800
Greg Clark _Farewell to Alms_: 
![bg center w:1200](attachments/gc_malawi_england_para.png)

---

#### Effect of lowered death rate


![bg right:50% w:650](attachments/gc_malthus_dr.png)

- Modern medicine (e.g. antibiotics, vaccines) has lowered death rates in poor areas.
- In a purely Malthusian setting, this leads to *lower* per-capita income
- Death rate falls (curve shifts down)
  - At initial $y_0^*$,  birth rate now exceeds new death rate
    - popn rises $N_0^*$ to $N_1^*$
    - income falls $y_0^*$ to new lower $y_1^*$ steady state.
- (Fortunately, health campaigns + new income generation often trigger transition. e.g. fewer kids, more time in school)
  
---

#### European Marriage and Fertility

![bg center w:900](attachments/gc_f4.2_age_marriage.png)

---

#### Why would modern day Malawi incomes be below English of 1800?

- Lots of explanations to be explored
- A simple Malthusian one:
  - modern medicine has lowered death rates but birth rates remain high.
  - $\Rightarrow$ higher population and lower incomes.


---
### 1. The Potato and the Irish Population
- Potatoes yielded 2–4x more calories per acre than grain; thrived in poor, damp Irish soil.

- Demographic Boom: Population doubled (4M to 8M+) between 1750–1845 as small plots could now support large families.

- The Lumper Monoculture: Dependence on a single, high-yield variety created a "genetic bottleneck" with zero disease resistance.

- The Blight: Phytophthora infestans arrived in 1845; the lack of genetic diversity caused total, rapid crop failure.


---
### Irish population

![bg center w:800](attachments/gr_irish_pop.png)


---

### 1. Pre-Famine Context and The Blight (1845–1848)

![bg right:40% w:500](attachments/gr_irish_pot1.png)

* **The Potato Trap:** High-calorie yields fueled a population surge to 8M+, but dangerous "Lumper" monoculture.
* **Colonial Tenancy:** A rigid land system left the Catholic majority as landless tenants-at-will, dependent on tiny plots.
* **The Blight:** *Phytophthora infestans* arrives in 1845, causing total collapse of the primary food source.
* **Productivity Crash:** Decimation of the potato crop destroyed real wages of the rural poor, causing immediate destitution.

---

### 2. The Great Famine

* **Entitlement Failure:** Starvation occurred amid plenty; Ireland remained a net **exporter** of grain and livestock to England.
* **Ideological Failure:** *Laissez-faire* policy and "Poor Laws" prioritized market mechanics and property rights over direct relief.
* **The "Clearing":** Rent defaults triggered mass evictions, allowing landlords to consolidate small plots into large-scale cattle grazing.
* **Demographic Scarring:** 1 million dead; 1 million+ emigrated. Population has never returned to its 1845 peak.
* **Political Aftermath:** Perceived British indifference fueled century-long resentment and Irish nationalist movements.

---
### 3. Malthusian Classical Orthodoxy 

* **The Malthusian Trap:** Famine was framed as a "natural check" on a population that had geometrically outstripped its food supply.
* **The "Iron Law":** Based on the *Iron Law of Wages*, officials feared that providing food would artificially lower mortality, leading to an even larger population collapse later.
* **New Poor Law (1834):** The Malthusian framework mandated that relief be "less eligible" (worse) than the lowest paid labor, forcing the starving into punitive workhouses.
* **Moralism:** High-ranking officials like Charles Trevelyan viewed the blight as a "divine mechanism" to forcibly modernize Irish social and property structures.

---
### The Black Death

![bg center w:900](attachments/tb_blackdeath.png)

---

### The Black Death
![bg center w:800](attachments/gc_black_death.png)

---
![bg right:40% w:550 ](attachments/gr_mapdeaths.png)

#####  Institutional change following the Black Death
- Elites attempted 'Seigneurial Reaction' to limit rise in real wages. But ultimately failed.
  - The Stature of Laborers, 1349 .
  - Serfdom dissappears in most West Europe
  - Emerged/hardened in parts of East Europe were landlords more powerful.
  - Voigtlander & Voth (2013) (slides below) argue Black Death led to new eqn:
    -  Higher death rate
    -  More urbanization
    -  HIgher per-capita incomes


---

![bg left:60% w:750](attachments/gc_f2.6_income_pop.png)

* English data 1200-1790s
* Note clear effects of the Black Death > 1340s
* Transition ~ 17th century
   * Population rising without falling income per capita
* Sustained rising income per capita > 1870s

---

![bg center w:900](attachments/gc_f3.1_english_wages.png)


---

#### Did plagues lead Europe to transition?
 

![bg w:600](attachments/title_3horsemen.png)
![bg  w:500](attachments/gr_horsemen.jpg)


---
### Did population shocks move the economy to a better steady state?
- Paper title play on *Four Horsemen of the Apocalypse* (symbolic representations of the end of times in Christian scriptures):  Conquest/Pestilence, War, Famine, Death.
  
- Argument: 
   - Normally death rate curve falls with income per capita $y$
   - But during 1350-1700 period **death rate curve at times rose with $y$**
     - **Plague**  $\rightarrow$ per-capita income $y \uparrow$ 
     - $y \uparrow \rightarrow$ **Urbanization** $\uparrow$  (e.g. rise manuf demand and trade)
       - mortality was higher in cities so urbanization drove up death rate
     - $y \uparrow \rightarrow$ **War** $\uparrow$  (e.g. more tax for wars), death rates up.
- Possible multiple-equilibria, a shock may move economy from low to high equilibrium.
---




### Wars and State Formation

Sociologist **Charles Tilly** estimates that over 1500-1800, European Great Powers were engaged in wars 9 of every 10 years.

- To succeed/survive, states compelled to develop more centralized and sophisticated organization
- Strong centralized states with modern bureaucratic administration emerged.


![bg right w:450](attachments/tilly_cover.png)

---

![bg center w:1200](attachments/abstract_3horsemen.png)


---
Shock to populaiton
![bg center w:1200](attachments/voth_3horse_steady.png)



---

### Escape

![bg center w:800](attachments/gr_escape.jpg)

---


## The Storm Beneath the Surface

![bg center w:500](attachments/og_kettle.png)

---


![bg center w:900](attachments/og_cogs_change.png)


---


## Quantys versus Qualys

- Quantys: 'be fruitful and multiply'
  - 4 children per family, 2 survive to adulthood
  - little investment in human capital
  - subsistence farmers, manual laborers, etc.
- Qualys: 2 children per family
  - 2 survive to adulthood
  - heavier time and resource investment in child productivity/earning capacity
  - blacksmiths, traders, carpenters.
- Both groups maintaining shares in the population

---
## Quantys versus Qualys
### Suppose technological development boosts demand for qualy services
- raises income or Qualys relative to Quantys (an evolutionary advantage)
- Over time raise family size from 2 to 3 children
- Still below rate of Quantys, but now more Qualy children reach maturity

Positive feedback loop
*  tech $\rightarrow$ Qualy incomes and population $\rightarrow$ more tech.



---


![bg center w:900](attachments/og_cogs2.png)




---
### Elements of Galor's Unified Theory

Population size and Composition foster progress via:
* supply of innovations
* Demand for innovations
* Diffusion of Knowledge
* Division of Labor
* Extent of Trade

Traits complementary to the growth process
(transmitted culturally as norms/customs)
  - Generated higher incomes
    - capital accumulation
    - future-orientation
  - Adaptation



- 

---
#### A simpler model

## From Malthus to Solow

- **Malthusian growth model:** Land and labor.
  - population growth is exponential, land is fixed (non-accumulated).
  - One time improvement in technology $A \rightarrow$ 
      - income per capita $y$ falls back toward subsistence.
      - long run growth in per-capita incomes essentially zero.
  

Example:
$$
Y = A\cdot T^\beta \cdot L^{1-\beta}
$$

but land $T$ is fixed, so $y = A \cdot \frac{1}{L^\beta}$

- Higher $A$ $\rightarrow$ $y$ rises temporarily, but eventually falls back to subsistence level.

---

## Solow Growth Model

The early main "neo-classical growth model":

- Production with labor and capital (could add human capital).
- Unlike land, capital can be accumulated via saving/investment. 
- New capital tools to equip expanding worker population. 
- But capital accumulates subject to diminishing returns.
- In steady-state 
  - Capital per worker will be constant $k=\frac{K}{L}$
  - Income-per capita $y$ constant at level above subsistence, despite pop growth.
  - Investment make up for capital depreciation and equip new workers.
  - Level determined by technology $A$, savings rate $s$, and depreciation rate $\delta$.


---

![bg center w:600](attachments/gr_solow.png)


---
![bg right:20% w:300](attachments/pic_solow.png)
- **Solow (neo-classical) growth model:** capital is accumulated.  
  - growing population of workers can be equipped with new capital.
    - capital accumulation subject to diminishing returns.
    - economy reaches steady-state level $y$ above subsistence.
  - One time improvement in technology $A \rightarrow$ $y$ rises to higher steady state.
  - Long run *growth* in per-capita income only with *sustained* technology improvement.

- Robert Solow (MIT), Nobel 1987
>"In the 1950s, he developed a mathematical model illustrating how various factors can contribute to sustained national economic growth. From the 1960s on, Solow’s studies helped persuade governments to channel funds into technological research and development to spur economic growth."

---
## Neo-classical growth model (expanded Solow model)

 * Predicts 'convergence' of per capita income across countries.  
   *-* Suppose two countries with same technology and same savings rate.
   * High capital/worker $k=K/L$ country is closer to steady-state. Grows slowly.
   * Country w/ low capital/worker $k=K/L$ further away to steady-state. Grows faster.
   * Model predicts **convergence** of per capita income over time.
  
  

---
## Neo-classical growth more generally

- Convergence in per-capita incomes across countries, via any that tends to equalize technology and capital/worker ratios across countries.  Market-based mehanisms will do the job:
  - **via capital accumulation** and/or international **capital flows**.
  - via **labor flows** across countries
  - via comparative advantage and **trade**. 

- Premised on no market failures and diminishing returns to capital.
- Development policy implications:
  - Let markets do their job: Liberalize, privatize, deregulate.
  - Poor countries are poor because of distortions to markets. 

