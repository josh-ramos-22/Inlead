// Adapted from 
// https://stackoverflow.com/questions/12409299/how-to-get-current-formatted-date-dd-mm-yyyy-in-javascript-and-append-it-to-an-i
const formatDate = (dateObj : Date) : string => {
  const yyyy = dateObj.getFullYear();
  const mm = dateObj.getMonth() + 1; // Months start at 0!
  const dd = dateObj.getDate();

  let ddStr = String(dd);
  let mmStr = String(mm);

  if (dd < 10) ddStr = "0" + ddStr;
  if (mm < 10) mmStr = "0" + mmStr;

  return ddStr + "/" + mmStr + "/" + yyyy;
};

// Adapted from
// https://stackoverflow.com/questions/8888491/how-do-you-display-javascript-datetime-in-12-hour-am-pm-format
const formatTime = (dateObj : Date) : string => {
  // Get time in 00:00 [am|pm] format
  let hours = dateObj.getHours();
  const minutes = dateObj.getMinutes();
  const ampm = hours >= 12 ? "pm" : "am";
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour "0" should be "12"
  const minutesStr = minutes < 10 ? "0" + minutes : "" + minutes;

  return hours + ":" + minutesStr + " " + ampm;
};

// Returns a date in a user friendly format
// DD/MM/YYYY at XX:XX [am|pm]
const prettyPrintDate = (isoString : string) => {
  const dateObj = new Date(isoString);

  let formattedDate = formatDate(dateObj);
  const formattedTime = formatTime(dateObj);

  // Change date to "Today" if appropriate
  const todayDateObj = new Date();

  const todayDate = formatDate(todayDateObj);
  if (formattedDate === todayDate) {
    formattedDate = "Today";
  } 
  
  return `${formattedDate} at ${formattedTime}`;
};

export default prettyPrintDate;