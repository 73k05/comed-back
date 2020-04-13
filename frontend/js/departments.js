// SELECT DEPARTMENT DATA
function populateSelect() {
    // THE JSON ARRAY.
    const departments = [
        { "Department_Name": "Ain" },
        { "Department_Name": "Aisne" },
        { "Department_Name": "Allier" },
        { "Department_Name": "Alpes-de-Haute-Provence" },
        { "Department_Name": "Hautes-Alpes" },
        { "Department_Name": "Alpes-Maritimes" },
        { "Department_Name": "Ardèche" },
        { "Department_Name": "Ardennes" },
        { "Department_Name": "Ariège" },
        { "Department_Name": "Aube" },
        { "Department_Name": "Aude" },
        { "Department_Name": "Bouches-du-Rhône" },
        { "Department_Name": "Calvados" },
        { "Department_Name": "Cantal" },
        { "Department_Name": "Charente" },
        { "Department_Name": "Charente-Maritime" },
        { "Department_Name": "Cher" },
        { "Department_Name": "Corrèze" },
        { "Department_Name": "Côte-d'Or" },
        { "Department_Name": "Côtes-d'Armor" },
        { "Department_Name": "Creuse" },
        { "Department_Name": "Dordogne" },
        { "Department_Name": "Doubs" },
        { "Department_Name": "Drôme" },
        { "Department_Name": "Eure" },
        { "Department_Name": "Eure-et-Loir" },
        { "Department_Name": "Finistère" },
        { "Department_Name": "Gard" },
        { "Department_Name": "Haute-Garonne" },
        { "Department_Name": "Gers" },
        { "Department_Name": "Gironde" },
        { "Department_Name": "Hérault" },
        { "Department_Name": "Ille-et-Vilaine	" },
        { "Department_Name": "Indre" },
        { "Department_Name": "Indre-et-Loire" },
        { "Department_Name": "Isère" },
        { "Department_Name": "Jura" },
        { "Department_Name": "Landes" },
        { "Department_Name": "Loir-et-Cher" },
        { "Department_Name": "Loire" },
        { "Department_Name": "Haute-Loire" },
        { "Department_Name": "Loire-Atlantique" },
        { "Department_Name": "Loiret" },
        { "Department_Name": "Lot" },
        { "Department_Name": "Lot-et-Garonne" },
        { "Department_Name": "Lozère" },
        { "Department_Name": "Maine-et-Loire" },
        { "Department_Name": "Manche" },
        { "Department_Name": "Marne" },
        { "Department_Name": "Haute-Marne" },
        { "Department_Name": "Mayenne" },
        { "Department_Name": "Meurthe-et-Moselle" },
        { "Department_Name": "Meuse" },
        { "Department_Name": "Morbihan" },
        { "Department_Name": "Moselle" },
        { "Department_Name": "Nièvre" },
        { "Department_Name": "Nord" },
        { "Department_Name": "Oise" },
        { "Department_Name": "Orne" },
        { "Department_Name": "Pas-de-Calais" },
        { "Department_Name": "Puy-de-Dôme" },
        { "Department_Name": "Pyrénées-Atlantiques" },
        { "Department_Name": "Hautes-Pyrénées" },
        { "Department_Name": "Pyrénées-Orientales" },
        { "Department_Name": "Bas-Rhin" },
        { "Department_Name": "Haut-Rhin" },
        { "Department_Name": "Rhône" },
        { "Department_Name": "Haute-Saône" },
        { "Department_Name": "Saône-et-Loire" },
        { "Department_Name": "Sarthe" },
        { "Department_Name": "Savoie" },
        { "Department_Name": "Haute-Savoie" },
        { "Department_Name": "Seine-Maritime" },
        { "Department_Name": "Seine-et-Marne" },
        { "Department_Name": "Yvelines" },
        { "Department_Name": "Deux-Sèvres" },
        { "Department_Name": "Somme" },
        { "Department_Name": "Tarn	" },
        { "Department_Name": "Tarn-et-Garonne" },
        { "Department_Name": "Var" },
        { "Department_Name": "Vaucluse" },
        { "Department_Name": "Vendée" },
        { "Department_Name": "Vienne" },
        { "Department_Name": "Haute-Vienne" },
        { "Department_Name": "Vosges" },
        { "Department_Name": "Yonne" },
        { "Department_Name": "Territoire de Belfort" },
        { "Department_Name": "Essonne" },
        { "Department_Name": "Hauts-de-Seine" },
        { "Department_Name": "Seine-Saint-Denis" },
        { "Department_Name": "Val-de-Marne" },
        { "Department_Name": "Val-d’Oise" },
        { "Department_Name": "Guadeloupe" },
        { "Department_Name": "La Réunion" },
        { "Department_Name": "Mayotte" }
    ];

    let element = document.getElementById('region');
    for (var i = 0; i < departments.length; i++) {
        // POPULATE SELECT ELEMENT WITH JSON.
        element.innerHTML = element.innerHTML +
            '<option value="' +departments[i]['Department_Name'] + '">' + departments[i]['Department_Name'] + '</option>';
    }
};
