# AIS-data-
En undersøkelse av AIS-data fra amerikanske kystmyndigheter (fra 01.01.2023), der jeg bearbeider rå CSV-data, strukturerer dataene og lager varmekart for å undersøke aktivitetsnivå og trafikkmønstre til sjøs.

I prosjektet bruker jeg python biblioteket aisdb, i tillegg til en wsl, da aisdb ikke fungerer på windows. Veiledning og inspirasjon til prosjektet finnes på https://aisviz.gitbook.io/documentation

Filbeskrivelser:

Creating_db: Omgjøring fra csv fil til en SQLite database. CSV-fil hentet fra https://hub.marinecadastre.gov/pages/vesseltraffic

Loading_DB: Behandling og visualisering av databasen samt vise domenet av interesse. Se 'visualisering av loading_DB' for visualisering.

AIS_heatmap/ais_heatmap_time: Kode for varmekart. Visualiseringen er eksportert som HTML og kan åpnes direkte i nettleser.
