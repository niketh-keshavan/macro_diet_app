document.getElementById("macro-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent form submission

    const carbs = document.getElementById("carbs").value;
    const protein = document.getElementById("protein").value;
    const fat = document.getElementById("fat").value;
    const dietType = document.getElementById("diet-type").value;

    // If "Any" is selected, send null for diet type
    const requestData = {
        macros: {
            carbs: parseFloat(carbs),
            protein: parseFloat(protein),
            fat: parseFloat(fat),
        },
        diet_type: dietType === "" ? null : dietType, // Convert empty string to null
    };

    try {
        const response = await fetch("/get_recipes", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(requestData),
        });

        const data = await response.json();

        // Update the results on the page
        const recipeList = document.getElementById("recipe-list");
        recipeList.innerHTML = ""; // Clear existing results

        if (data.meals.length > 0) {
            const totalMacrosDiv = document.createElement("div");
            totalMacrosDiv.innerHTML = `<h3>Total Macros:</h3>
                <p>Carbs: ${data.total_macros.carbs}g</p>
                <p>Protein: ${data.total_macros.protein}g</p>
                <p>Fat: ${data.total_macros.fat}g</p>`;
            recipeList.appendChild(totalMacrosDiv);

            data.meals.forEach((meal) => {
                const listItem = document.createElement("li");
                listItem.textContent = `${meal.name} - Carbs: ${meal.macros.carbs}g, Protein: ${meal.macros.protein}g, Fat: ${meal.macros.fat}g`;
                recipeList.appendChild(listItem);
            });
        } else {
            recipeList.innerHTML = "<li>No matching meal combinations found</li>";
        }
    } catch (error) {
        console.error("Error fetching recipes:", error);
    }
});
