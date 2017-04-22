# Le fix me

J'ai testé ceci avec un système en local FTP/HTTP (2121/8080). Chose que vous n'avez pas faite.

## Installation

- Il y a un README \o/!
- L'installation est prévue pour sqlite... un bon conseil développez dans l'environnement le plus réel possible.
- la branche deploy pourrait faire partie de master (à base de `if`)

## Python

- FTPManager possède quatre fonctions et autant de ftp.connect...
- try/except sans spécifier l'exception, c'est risqué.
- la gestion des erreurs est tristement baclée

  - les droits d'écritures sur le FTP ne sont pas forcément présents.
  - un mot de passe peut changer

- sans html5lib impossible de parser du code comme celui-ci: <https://google.github.io/styleguide/htmlcssguide.html#HTML_Validity>

- with c'est bon, mangez-en!

- vous avez quatre fois `render(website/configure.html)` c'est deux fois trop si on admet que création et modification peuvent partager un template.

## UX

- Le bookmark pert le port... cassé.
- Un site web non servi sur le port 80 est difficile à utiliser (e.g. <http://localhost:8080/>)
- Pourquoi un menu en drop-down en mode écran?
- Pourquoi le bouton save nous fait quitter l'éditeur?
- Pourquoi l'éditeur est-il si lent à apparaitre?
- Pourquoi l'éditeur ne ressemble-t-il pas à mon site web modifié?
- Un seul sélecteur est hyper-limitant. Par exemple, modifier `<title>` serait important.
- Vous auriez pu pousser l'édition plus loin avec une gestion d'un historique.
