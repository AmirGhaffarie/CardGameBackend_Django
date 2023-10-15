document.addEventListener('DOMContentLoaded', function() {
    let groupField = document.getElementById("id_group");
    let idolField = document.getElementById("id_idol");
    let eraField = document.getElementById("id_era");

    function updateIdolAndEraOptions() {
        let selectedGroupId = groupField.options[groupField.selectedIndex].value;
        
        // Clear existing options
        while (idolField.firstChild) {
            idolField.removeChild(idolField.firstChild);
        }
        while (eraField.firstChild) {
            eraField.removeChild(eraField.firstChild);
        }
        
        // Add new options based on the selected group
        if (selectedGroupId) {
            let xhr = new XMLHttpRequest();
            xhr.open('GET', '/base/get_idols/?group_id=' + selectedGroupId, true);
            xhr.onload = function() {
                let subgroups = JSON.parse(xhr.responseText);
                subgroups.forEach(function(subgroup) {
                    let option = document.createElement('option');
                    option.value = subgroup.id;
                    option.text = subgroup.name;
                    idolField.add(option);
                });
            };
            xhr.send();

            let xhr2 = new XMLHttpRequest();
            xhr2.open('GET', '/base/get_eras/?group_id=' + selectedGroupId, true);
            xhr2.onload = function() {
                let subgroups = JSON.parse(xhr2.responseText);
                subgroups.forEach(function(subgroup) {
                    let option = document.createElement('option');
                    option.value = subgroup.id;
                    option.text = subgroup.name;
                    eraField.add(option);
                });
            };
            xhr2.send();
        }
    }

    updateIdolAndEraOptions();
    // Add event listener to the group field
    groupField.addEventListener('change', updateIdolAndEraOptions);
});