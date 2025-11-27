// // Récupération de l'élément HTML ayant pour ID 'department' (menu déroulant)
// const department = document.getElementById("department");

// // Fonction anonyme asynchrone
// department.addEventListener("change", async () => {
//   // Récupération de la valeur choisie par l'utilisateur dans le menu déroulant
//   const depValue = department.value;
//   // console.log("Valeur envoyée :", depValue);

//   // Préparation d'un formulaire vide
//   const formData = new FormData();

//   // Ajout de la valeur choisie par l'utilisateur dans le formulaire comprenant
//   // une clé ('commune') et une valeur (celle choisie par l'utilisateur),
//   // similaire à un dictionnaire de Python
//   formData.append("department", depValue);

//   try {
//     // Requête HTTP asynchrone : POST vers l'URL '/city'
//     const res = await fetch("/city", {
//       method: "POST",
//       body: formData /* Envoi du formulaire complété... */,
//       headers: {
//         Accept: "application/json" /* ...transmis sous la forme JSON */,
//       },
//     });

//     // Si la réponse n’est pas "OK" (statut HTTP 2xx),
//     // on provoque une erreur qui sera prise en charge par le catch
//     if (!res.ok) throw new Error(`HTTP ${res.status}`);
//     const data = await res.json();
//     console.log("Réponse du serveur :", data);

//   } catch (err) {
//     console.error("Erreur :", err);
//   }
// });

const department = document.getElementById("department");
const citySelect = document.getElementById("city");

department.addEventListener("change", async () => {
  const depValue = department.value;
  const formData = new FormData();
  formData.append("department", depValue);

  try {
    const res = await fetch("/city", {
      method: "POST",
      body: formData,
      headers: { Accept: "application/json" },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    // Affichage dynamique des villes
    citySelect.innerHTML = ""; // Vide la liste actuelle
    if (data.city_list.length > 0) {
      data.city_list.forEach((ville) => {
        const option = document.createElement("option");
        option.value = ville;
        option.textContent = ville;
        citySelect.appendChild(option);
      });
    } else {
      const option = document.createElement("option");
      option.textContent = "Aucune commune trouvée";
      citySelect.appendChild(option);
    }
  } catch (err) {
    console.error("Erreur :", err);
  }
});
