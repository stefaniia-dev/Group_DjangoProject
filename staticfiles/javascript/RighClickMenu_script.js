let WeeklyEvents = document.querySelectorAll(".eventBoxes");
let Goals = document.querySelectorAll(".goals");
let Logs = document.querySelectorAll(".logs");
let Event_Right_Click_Menu = document.querySelectorAll(".EventRightClickMenu")
let Logs_Right_Click_Menu = document.querySelectorAll(".LogsRightClickMenu")

function Menu(i, topPosition, leftPosition){
            console.log(" 1 event: ", Event_Right_Click_Menu[i])
        //Turns on context menu
        Event_Right_Click_Menu[i].classList.add("active")

    //Position
        Event_Right_Click_Menu[i].style.top = topPosition + "px";
        Event_Right_Click_Menu[i].style.left = leftPosition + "px";

//Closes window when you click somewhere else
        window.addEventListener("click", () => {
    Event_Right_Click_Menu[i].classList.remove("active");
})

}


console.log("logs", Logs);
console.log("Logs_Right_Click_Menu", Logs_Right_Click_Menu);

function LogsMenu(i, topPosition, leftPosition){
        //Turns on context menu
        Logs_Right_Click_Menu[i].classList.add("active")

    //Position
        Logs_Right_Click_Menu[i].style.top = topPosition + "px";
        Logs_Right_Click_Menu[i].style.left = leftPosition + "px";

//Closes window when you click somewhere else
        window.addEventListener("click", () => {
    Logs_Right_Click_Menu[i].classList.remove("active");
})

}


console.log("goals", Goals)
console.log("Event_Right_Click_Menu", Event_Right_Click_Menu)



// ------------------- Weekly events addEvent listener ---------------------
for (let i = 0; i < Logs.length; i++) {

    //Adds event listener to each  Event being displayed
    Logs[i].addEventListener("contextmenu", (event) => {

        event.preventDefault();//prevents regular right click menu from appearing
        event.stopPropagation(); //important!!

        console.log("before active i: ", i)

        console.log("after active i: ", i)
        //Position of the menu
        let topPosition = event.clientY;
        let leftPosition = event.clientX;


        //Displays and closes context menu and positions it
        LogsMenu(i, topPosition, leftPosition);

    });
}









// ------------------- Goals addEvent listener ---------------------
for (let i = 0; i < Goals.length; i++) {

    //Adds event listener to each  Event being displayed
    Goals[i].addEventListener("contextmenu", (event) => {

        event.preventDefault();//prevents regular right click menu from appearing
        event.stopPropagation(); //important!!

        console.log("before active i: ", i)

        console.log("after active i: ", i)
        //Position of the menu
        let topPosition = event.clientY;
        let leftPosition = event.clientX;


        //Displays and closes context menu and positions it
        Menu(i, topPosition, leftPosition);

    });
}


// ------------------- Weekly events addEvent listener ---------------------
for (let i = 0; i < WeeklyEvents.length; i++) {

    //Adds event listener to each  Event being displayed
    WeeklyEvents[i].addEventListener("contextmenu", (event) => {

        event.preventDefault();//prevents regular right click menu from appearing
        event.stopPropagation(); //important!!

        //Position of the menu
        let topPosition = event.clientY;
        let leftPosition = event.clientX;


        //Displays and closes context menu and positions it
        Menu(i, topPosition, leftPosition);

    });
}


