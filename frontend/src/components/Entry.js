import React from 'react';

function Entry(props) {
  
  return(<div className="entryBox">
    On {props.entry.night}, you slept for {props.entry.duration} hours.     
    <button style={{'position':'absolute', 'left':'35vw'}} onClick={() => props.updateCallBack(props.id)}>Update</button>
    <button onClick = {() => props.deleteEntry(props.id)} style={{'position':'absolute', 'left':'40vw'}}>Delete</button>

  </div>);
}

export default Entry