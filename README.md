# Mangmap

## Configuration

Le site est globalement configurable à l'URL [http://adresse-du-site.fr]/admin.

De nombreux éléments contiennent un champ `slug`, cela correspond à un champ technique, qui doit être unique par type
d'élément. En général, c'est le nom de l'élément, en anglais, en miniscule.

### Les sites

Depuis le menu de gauche, il y a un sous-menu "Sites". Ce sous-menu possède trois éléments :
sites, thématiques et types de sites.

A priori, les thématiques sont fixes. En tout cas, d'éventuels ajout ne bénéficieraient pas de logo. Les types de
sites sont plus flexibles car il n'y a pas d'image associée et peuvent donc être configués.

Une site doit avoir un fichier lié ou un lien.

### Les actualités

De la même manière, les actualités sont configurés dans le sous-menu Actualités.

### Pays, profils et zones du monde

Les pays, profils et zones du monde sont configurables dans le sous-menu "Général".

De la même manière que les thématiques de sites, les zones du monde ne sont pas prévues pour être changées, hormis
leur nom.

### Utilisateurs admin

La gestion des utilisateurs se fait depuis le sous-menu Paramètres, puis Utilisateurs. Le plus simple est ensuite de
donner tous les droits aux administrateurs. Depuis l'édition ou l'ajout d'un utilisateur, aller dans l'onglet Rôles, et
cocher toutes les cases.

### Les pages annexes (mentions légales, données personnelles)

Ces pages peuvent être ajoutées / modifiées en créant / modifiant une page de contenu avec comme slug :

- `mentions-legales` pour les mentions légales
- `donnees-personnelles` pour les données personnelles


## Pour les développeurs

### Mettre à jour les traductions :

- Créer ou mettre à jour un fichier de traductions (à faire pour chaque langue, `fr` ou `en`) :
    `django-admin makemessages -l fr`
- Renseigner à la main les traductions dans les fichiers .po autogénéré
- Compiler les fichiers de traductions:
    `django-admin compilemessages`

### Mettre à jour les fichiers Bulma :

- `cd generate_bulma_css/`
- `yarn install`
- `yarn css-build`
- `yarn minify`