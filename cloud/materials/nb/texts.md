# Many Worlds Cloud · Norsk (bokmål)

## Slagord
- Vit hva som er eksponert i skyen, og hva som bør gjøres med det.
- Fra tusenvis av kontroller som feiler, til tre lister dere kan handle på.
- Uskannet vises aldri som rent.

## Kort beskrivelse
Many Worlds Cloud analyserer det Prowler, skanneren med åpen kildekode, finner i skykontoene deres, og gjør det om til en rapport og en liste over ting å handle på: risikoer, hendelser og oppgaver.

## Middels beskrivelse
Many Worlds Cloud gjør sikkerhetsskanninger av sky om til beslutninger. Prowler, skanneren med åpen kildekode, kontrollerer kontoene deres i AWS, Azure, Google Cloud, Kubernetes og Microsoft 365 med en rolle som bare kan lese. Many Worlds Cloud analyserer resultatene og skriver en rapport som begynner med hvor fullstendig skyen kunne skannes, rangerer funnene etter alvorlighet og ender i tre lister: risikoer til registeret, hendelser til SOC og oppgaver til en kø. Én knapp sender dem til SpaceRisk.

## Lang beskrivelse
En sikkerhetsskanner for sky gir tusenvis av rader, og det kan ingen ta beslutninger ut fra. Many Worlds Cloud analyserer det Prowler, skanneren med åpen kildekode, finner i skykontoene deres, og gjør det om til en rapport som tre slags lesere kan bruke. Ledelsen får et ledersammendrag som svarer på én side: går risikoen opp eller ned, hva er åpent mot internett, hvem har administratortilgang. Skyeiere får en visning som går ned til den enkelte ressursen. De som gjør jobben, får den fullstendige rapporten med bevisene. Hver rapport åpner med hvilke kontoer som ble skannet, og hvilke kontroller som ikke kunne kjøres, så en uskannet konto aldri vises som ren. Funnene rangeres etter alvorlighet, hvert med hvorfor det betyr noe, hva som bør gjøres, og bevisene, og knyttes til rammeverk som CIS, ISO 27001, NIS2 og ENS. Rapporten ender i tre lister: risikoer, hendelser og oppgaver. Én knapp sender dem til et SpaceRisk-register, og det finnes eksport til SIEM, Jira, ServiceNow, Excel og PowerPoint. Many Worlds Cloud bare analyserer. Den kjører på egen server og endrer ingenting i skyen.

## Funksjoner
- **Den bare analyserer:** Ingenting installeres i skyen, og ingenting i den endres. Prowler skanner hver skykonto med en rolle som bare kan lese. Many Worlds Cloud analyserer resultatene. Den skriver aldri til kontoene deres, og den ber aldri om hemmelighetene den finner, bare om hvor de ligger.
- **Kan man stole på resultatene?:** Rapporten begynner med å si hvor fullstendig skyen kunne skannes. En konto som er stille fordi skanningen feilet, må aldri leses som en konto uten feil. Derfor åpner hver rapport med hvilke kontoer som ble skannet, når, og hvilke kontroller som ikke kunne kjøres.
- **Funn, rangert etter alvorlighet:** Hvert funn kommer med hvorfor det betyr noe, hva som bør gjøres, og bevisene. Et funn er noe skanningen observerte som krever en beslutning. De verste kommer først, og hvert funn kan spores til ressursen og kontrollen bak det.
- **Etterlevelse:** Se hvilke krav dere oppfyller, og hvilke dere ikke oppfyller. Prowler knytter kontrollene sine til rammeverkene revisorer spør om. Rapporten viser hvert rammeverk krav for krav, med funnene bak hvert krav som feiler.
- **Konklusjoner:** Rapporten ender i tre lister som noen kan handle på. Risikoer går til et register, hendelser til en SOC og oppgaver til en kø. Hver vurdering har med regelen som ga den.
- **Alle kontoer samtidig:** Ranger skykontoene etter hva som må avgjøres. Med mer enn én konto, ett abonnement eller ett prosjekt vises de side om side: hvilken som trenger oppmerksomhet først, hva som gjelder flere av dem mot hva som gjelder én, og hvilke som ikke kunne skannes fullstendig.

## Standardtekst
Om Many Worlds Cloud: Many Worlds Cloud er et rapporteringsverktøy for skysikkerhet. Det analyserer resultatene fra Prowler, skanneren med åpen kildekode for skysikkerhet, og gjør dem om til en rapport med tre visninger og tre lister å handle på: risikoer, hendelser og oppgaver. Det kjører på egen server, bare analyserer, og kan sende konklusjonene til et SpaceRisk-risikoregister. Many Worlds Cloud er en del av Many Worlds-familien fra Frivold Digital, sammen med Many Worlds Historian og Many Worlds Identity.
