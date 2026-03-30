let currentDate = new Date; //start from current user's device date
var numOfEvents = 0; //counter for number of events on a specific day
var buttonAppearedAlready = false; //boolean for viewMore button

function generateCalendar(newDate) {
    //retrieve the current newDate and calculate/retrieve all of its information
    const month = newDate.getMonth(); // 0 - 11
    const year = newDate.getFullYear();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDay = firstDay.getDay();

    const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    //update month name h2 tag in html with the correct month and year
    document.getElementById("month_name").querySelector("h2").innerText = months[month] + ' ' + year;

    //clear previous calendar by redefining the calendarGrid for a new one
    const calendarGrid = document.getElementById('calendar_grid');
    //fixed display of all the days of the week
    calendarGrid.innerHTML = '<p>Sunday</p><p>Monday</p><p>Tuesday</p><p>Wednesday</p><p>Thursday</p><p>Friday</p><p>Saturday</p>';

    for (let i = 0; i < startingDay; i++) {
        calendarGrid.innerHTML += '<p></p>'; //empty squares for days before the first of the month
    }

    //add all the rest of the days to the calendarGrid
    for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement("div");
        dayCell.className = 'day';
        dayCell.setAttribute('data-day', day); //basically creating an attribute of each daycell to contain the event data specific to that day
        dayCell.innerText = day.toString();

        let currCylceDate = new Date();
        currCylceDate.setDate(day);

        //debug statements to check between currentDate and the currCycleDate
        /*
        console.log("currCycleDate is: " + currCylceDate);
        console.log("dayNum is: " + day);
        console.log(("currentDate is: " + currentDate));
        */

        //if the current date of the iteration is the same as the current real life date
        if (currCylceDate.getDate() === currentDate.getDate() && currCylceDate.getMonth() === currentDate.getMonth() && currCylceDate.getFullYear() === currentDate.getFullYear()) {
            dayCell.classList.add('highlight'); //add highlight class to the matched dayCell
        }

        calendarGrid.appendChild(dayCell);
    }

    $(document).ready(function () {
        $.ajax({
            type: 'GET',
            url: "http://127.0.0.1:8000/displayEvents/",//gets display events link so that it can render the data
            success: function (response) {
                $("#display").empty();

                for (let dayNum = 1; dayNum < daysInMonth; dayNum++) { //loop through each day individually

                    for (var key in response.events) { //loop through all the events in the database
                        const eventDate = new Date(response.events[key].date_of_event.replace(/-/g, '\/')) //save the date of the event

                        //basically creating a new date variable to hold the current calendar date of this big for loop
                        //it keeps track of the date the for loop is currently iterating through (aka the calendar date based on dayNum)
                        let CurrentCalendarDateFull = new Date();
                        CurrentCalendarDateFull.setDate(dayNum - 1); //attach dayNum to the day part of CurrentCalendarDateFull
                        //parse the date to be YYYY-MM-DD format so that weekly_schedule can process it properly
                        let parsedDate = CurrentCalendarDateFull.toISOString().split('T')[0];

                        //debugging for checking the dates being passed to weekly_schedules
                        //console.log("calendarDateFull is:" + CurrentCalendarDateFull);
                        //console.log("parsed date is:" + parsedDate);

                        if (eventDate.getMonth() === month && eventDate.getFullYear() === year && eventDate.getDate() === dayNum) { //check if the date of the event is the same as the day
                            //if yes

                            //get the dayCell for the corresponding day
                            const dayCell = document.querySelector(`.day[data-day="${dayNum}"]`);

                            if (dayCell && numOfEvents < 3) { //won't keep displaying events in the dayCell if more than 3 are already being displayed

                                //retrieve the event data for that day
                                const eventHTML = `<li>${response.events[key].event_name}</li>`; //displays name of the event

                                //debug statements to check what data is being passed around
                                /*
                                console.log("event name being passed is: " + response.events[key].event_name); //correct
                                console.log("event date being passed is: " + response.events[key].event_date); //undefined
                                console.log("event date being passed is: " + parsedDate); //correct
                                console.log("event description being passed is: " + response.events[key].description); //correct
                                */

                                //passes each detail of the event individually to the viewEventDetailsWidget function
                                //AND
                                //adds the event data to the daycell day data
                                let EventID = response.events[key].id;
                                // let UpdateUrl = "/updateEvent/ pk ".replace('pk', EventID);
                                dayCell.innerHTML += `<button class="event_as_button" onclick="viewEventDetailsWidget('${response.events[key].event_name}', '${parsedDate}', '${response.events[key].description}', '${response.events[key].id}', '${response.events[key].id}')"><a>${eventHTML}</a></button>`;

                            }

                            numOfEvents += 1
                            console.log("number of events is:" + numOfEvents + " day number is:" + dayNum);

                            if (numOfEvents > 3 && buttonAppearedAlready === false) { //if the number of events for that specific day is > 3, and the 'viewmore' button has not been displayed yet
                                ShowViewMore(); //toggle the view more button ON
                                buttonAppearedAlready = true; //so that the view more button only appears once for that day
                                console.log("parsed date BEFORE BUTTON is:" + parsedDate);

                                //view more button that passes the parsed (YYYY-MM-DD) version of CurrentCalendarDateFull to weekly_schedule
                                //directs to the weekly_schedule page that corresponds to CurrentCalendarDateFull
                                dayCell.innerHTML += `<a href="/weekly_schedule/?date=${parsedDate}" id="vmButton" style="color: #254B5B;
                                                                                                     font-style: italic">View More</a>`
                            } else {
                                //if no, keep the view more button toggled OFF
                                HideViewMore();
                            }
                        }
                        //if no, take the next event in the database and check again
                    }
                    numOfEvents = 0; //reset the event counter for the next day
                    buttonAppearedAlready = false; //reset the button press for the next day
                }
            },
            error: function (response) {
                alert("error")
            }
        });
    })
}

function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1); //increases the value of month (0-11)
    generateCalendar(currentDate);
}

function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1); //decreases the value of month (0-11)
    generateCalendar(currentDate);
}

window.onload = function () {
    generateCalendar(currentDate);
}

function ShowViewMore() {
    var button = document.getElementById("vmButton");
    button.style.display = "block";
}

function HideViewMore() {
    var button = document.getElementById("vmButton");
    button.style.display = "none";
}

function viewEventDetailsWidget(eventName, parsedDate, eventDesc, eventUpdate, eventDelete) {
    //Event Info
    var eName = document.getElementById("event_name_wg");
    var eDate = document.getElementById("event_date");
    var eDesc = document.getElementById("event_desc");

    // Update and delete
    var eUpdate = document.getElementById("UpdateEventID");
    var eDelete = document.getElementById("DeleteEventID");

    eName.innerText = eventName;
    eDate.innerText = parsedDate;
    eDesc.innerText = eventDesc;

    // Update and delete
    eUpdate.innerHTML += '<a href ="/updateEvent/ pk">Update</a>'.replace('pk', eventUpdate);
    eDelete.innerHTML += '<a href ="/deleteEvent/ pk">Delete</a>'.replace('pk', eventDelete) ;



    //show the modal
    document.getElementById("view_event_details").showModal();
}


