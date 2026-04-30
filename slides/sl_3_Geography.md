---
title: sl_3_geography
description: "ECO 331: Economic History - sl_3_geography"
author: "Jonathan Conning"
deploy: true
title_custom: true
tags: [slides/final]
created: 2023-01-27T02:00:38.712Z
modified: 2025-01-30T14:00:00.000Z
marp: true
paginate: true
---

<!--
theme: gaia
paginate: true
footer: Eco 331: Neolithic Revolution, Early States
style: |
  section {font-size: 26px;}
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
-->

<!-- footer: "" -->



![bg right w:550 Image of Sl3 River-Basins](attachments/sl3_river-basins.jpg)

# ECO 331
## Economic History

```
GEOGRAPHY
```
Jonathan Conning
Spring 2026

---
### Readings


- OG 10 "The Shadow of Geography"
- KR 2 "Did Some Societies Win the Geography Lottery" (19-36)
- National Geographic (2015) _Guns, Germs, and Steel_. Episode 1 of 3, especially 29:41-end. (video link.)

<!-- 
## Large Language Models
* Amazing tools.  Use them !  
	* Great for filling in historical knowledge. Digging deeper.
	* Interact. Follow up and debate.
* [Gemini](https://gemini.google.com/), [Claude](https://claude.ai/), [ChatGPT](https://chatgpt.com/), [Open Meta](https://www.meta.ai/), [Deepseek](https://chat.deepseek.com/), [Mistral](https://chat.mistral.ai/chat)
	* Free, have free tier, or free trial.
* Do not substitute for reading (but do use to dig deeper).
* Write your own questions/comments. 
	* I can spot, and will penalize, generic answers!
-->
---
### Fundamental versus Proximate Causes of Growth

* Proximate Causes
  * Capital and Human Capital Accumulation
  * Trade and Specialization
  * Technological Innovation

* But what causes these things to happen?

* Candidates: Geography, Institutions, Culture, Demography.


---
### Geography Questions

- What geography features constrain/enable economic growth?
	- What are the causal mechanisms?
	- What is Jared Diamond's main thesis?
- Is geography fate?  Can transport infrastructure reverse effects?  
- Do places that require more cooperation to overcome environmental hardships have an advantage or disadvantage?
- Does better geography raise the level and/or the growth rate?

---

## A simple primer on linear regression

Suppose we have data on students scores on a midterm and a final.

![bg right w:600 Image of Gr Reg1](attachments/gr_reg1.png)

---
We hypothesize 



![bg right w:600 Image of Gr Reg0](attachments/gr_reg0.png)


Linear Regression to fit a hypothesized linear relation of the form

$$
y_i = a + b_1 \cdot x_i + e_i
$$


where:

$y_i$ = final exam score
$x_i$ = midterm exam score
$e_i$ = i.i.d. error

---
Students w/ high attendance (orange) have on avg. higher scores:

![bg right w:600 Image of Gr Reg3](attachments/gr_reg3.png)


---
## Revised model 
- Controls for a previously omitted variable 

![bg right w:600 Image of Gr Reg4](attachments/gr_reg4.png)

$$
y_i = a + b_1 \cdot x_i + b_2 \cdot D_i + e_i
$$

$y_i$ = final exam score
$x_i$ = midterm exam score
$D_i$ = 1 if attended regularly
$e_i$ = error term


---

![bg left w:550 Image of Gr Reg4](attachments/gr_reg4.png)
![Image of Reg Table2](attachments/reg_table2.png)


If `class` dummy is omitted; estimated $b_1$ coefficient biased upward. 

![Image of Reg Table](attachments/reg_table.png)

---

![bg w:600 Image of Correlation1](attachments/correlation1.png)
![bg w:600 Image of Correlation2](attachments/correlation2.png)


---
## Econometric Challenges

  - Identification challenges: are estimated effects causal and unbiased.
   -   Spurious correlation or Causation?
	   - Are the regressors exogenous or Endogenous? 

- Biased estimates might be due to:
  - omitted variables
  - selection or endogeneity bias 
    e.g. is $x_i$ variable exogenous (like the weather) or determined by same unobserved factors that affect $y_i$ 

---
## Does ice-cream explain pool drownings?

* ice-cream consumption jointly determined with pool drownings
* both are affected by temperature
    * when weather is hot
      * more pool use and drownings
      * more ice-cream consumption


![bg right w:700 Image of Gr Icecream Drownings](attachments/gr_icecream_drownings.jpg)


---

## Empirical Methodology: Difference-in-Differences
Recall Allen et al (2023) “The Economic Origins of Government.” 

![bg right w:650 Image of Diff In Diff](attachments/diff_in_diff.png)

- 1374 grid cells covering Tigris-Euphrates area
- 31 historical periods, 5000 BCE to 1950 CE
- Compare treated (river shifted toward) vs. control areas
- How much did the shift *increase* state formation?


---

![bg center w:800 Image of Mesopotamia Effects](attachments/mesopotamia_effects.png)


---
## Machine learning versus econometrics

- ML (including neural networks) is a new term for *applied predictive modeling*.
  - ML values robust prediction accuracy. 
  - Searches through very flexible non-linear models to find best 'fit'.
  - but generally not for causal identification or unbiased estimate of impacts.
  - If ice-cream helps predict drownings, model will use ice-cream.
  - Not useful for policy: Prohibit ice-cream will not reduce drownings!
- Econometrics is for hypothesis-testing.
  - Economist uses theory and evidence to posit an identified causal relationship
  - Uses statistical inference methods to obtain unbiased estimates of causal model parameters and tests hypothesised relationships.



---
### Geography and Economic Development
![bg right w:700 Image of Kr F2 1](attachments/Kr_F2_1.png)
* How does geography shape development?
* Jeff Sachs (Columbia) observes many poorest countries are landlocked.
* Water-based the most cost-effective transport, so a major disadvantage.
---


![bg center w:1200 Image of Map Co2](attachments/map_CO2.png)
---

---
![bg center w:900 Image of Map Us Waterways](attachments/map_US_waterways.png)


---
next slide:

### India's Ganges River Basin

- One of the most fertile places on earth
- Hot (at same latitude as deserts)
- But moist due to monsoon rains off the Arabian sea


---

<div class="columns">
<div class="columns-left">

## River Basins

![w:450 Image of Gr India Basin](attachments/gr_India_basin.jpeg)
[Source](https://twitter.com/tomaspueyo/status/1622753371663867905)

</div>
<div class="columns-right">


## Population Density


![w:550 Image of Gr India Pop](attachments/gr_India_pop.jpeg)


</div>
</div>


---
<!-- iframe not visible in preview, use --html option in marp cli -->

<iframe width="700" height="394" src="https://www.youtube.com/embed/yLGSDtCiswA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

[Population through the ages video](https://www.youtube.com/watch?v=PUwmA3Q0_OE)


---

## Geography and Disease Environment
![bg right w:650 Image of Kr F2 2](attachments/kr_F2_2.png)

* Geography determines disease environment.
* Malaria has likely killed more than any other cause.
* Malaria belt regions grow as much as 1.3% slower (Gallup and Sachs, 2001).
* By reducing population density, delayed state formation.

---


![Image of Tsetse Abstract](attachments/tsetse_abstract.png)

---

![bg right Image of Tsetse2](attachments/tsetse2.png)

## Geography and Disease Environment

* tsetse fly causes sleeping sickness.
* kills livestock
* Impacts economic development and political formation
* Where fly is active less likely to develop large-scale states (Alsan, 2014)
---
### Jared Diamond
### Guns, Germs, and Steel

* Shape of Continents determined speed of technological diffusion.

![bg right w:800 Image of Kr F2 3](attachments/kr_F2_3.png)

---
![bg center w:1200 Image of Kr F2 4](attachments/kr_F2_4.png)

---


 ![bg center w:900 Image of Og F17](attachments/og_F17.png)

---
## Geography and Climate

![bg right:40% w:500 Image of Kr Temp](attachments/kr_temp.png)
* Climate changes.
* Roman Empire arose during period of exceptionally warm weather.
  * Decline during colder period
* After 1000 CE warmer weather again, higher yields and growth in  W Europe.
* Colder weather spells $\Rightarrow$ negative econ shocks.
  * Conflict, pogroms...

---
### Geography and Transport Infrastucture

* Geography matters but can be adapted
* Investment in transport infrastructure can reduce barriers to trade.
* Roman Road building
* Persistent long effects: 
  * European road network until 19th Century
  * Location of cities
  * Positive and Negative effects

---

![bg w:550 Image of Kr F2 6](attachments/kr_F2_6.png)
![bg w:550 Image of Map Roman](attachments/map_roman.png)

---

![bg center w:950 Image of Kr F2 7](attachments/kr_F2_7.png)

---

![bg center w:800 Image of Kr F2 9](attachments/kr_F2_9.png)


---

### The Columbian Exchange
## The Potato

(Friday presentation)
![bg right w:600 Image of Potato Woman](attachments/potato_woman.png)

<!--
---
![bg w:600 Image of Potato1](attachments/potato1.png)


---

![bg center w:900 Image of Potato2](attachments/potato2.png)

---

![bg center w:1000 Image of Potato3](attachments/potato3.png)


---

![bg center w:800 Image of Kr F2 9](attachments/kr_F2_9.png)

-->

---

## Centralization vs Competition
- Landscape fragmentation and the rise of Europe (Hume, Tilly)
    - Competition (vs Incumbent Monopolist)
      - Military
      - Public goods to attract population
      - Entrepreneurs, scientists, shopped regions.
  - Witfogel hydraulic hypothesis. Fractal coastline.
- Is geographical connectivity a benefit or a disadvantage?

---
### Origins of Extractive vs. Inclusive Institutions
- Did agroclimate shape institutions in US South, Latin America?
- Did geography/disease environment affect where colonization left 
  
---
## Geography, Crops, and future-orientation
* Future orientation: People from areas with higher _potential_ caloric return appear to be more future-oriented (from surveys).
  * Reverse causality?  
* Gender roles
  * Ploughs vs hoes and rakes.
  * World Values Survey suggests gender biases correlate.
    * Even in second-generation immigrants from countries that used the plough.


---

### Next class Readings

<br></br>
- OG 2 "Lost in Stagnation" 27-41
- OG 3 "The Storm Beneath the Surface", 43-55.
- (optional) KR 5 Fewer Babies?

Student focus paper: 

- Nunn, Nathan, and Nancy Qian. 2011. “The Potato’s Contribution to Population and Urbanization: Evidence from a Historical Experiment.” _The Quarterly Journal of Economics_ 126 (2): 593–650. ([PDF](https://drive.google.com/file/d/12EekL6XUzBIVkm4TMWyZndTCTvR5xkXI/view?usp=sharing))

---
### Population and growth Questions 1

- What is the "Malthusian Trap?"  
- What key elements of human demography and economic history does it explain?
- What are key assumptions of the model?
- Steady states and level versus growth effects
- Malthusian comparative statics
  - effect of raising/lowering birth rate?
  - effect of raising/lowering death rate
  - effect of raising/lowering technological productivity
- Date of onset of agriculture and expansion?