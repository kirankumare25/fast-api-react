import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios';



function GetAllUsers() {
  const GetAll = () => {
    window.location.href = "http://localhost:8000/user/details"
  }

  return (
    <div className='GetAllUsers'>
      
      <button onClick={GetAll}>Get All Users</button>
      
    </div>
  );
}


function GetUsers() {
  const [inputValue, setInputValue] = useState();

  const handleEvent = (event) =>  {
    setInputValue(event.target.value);
  }

  const handleNum = () => {
    if (inputValue){
       window.location.href = `http://localhost:8000/user/details/${inputValue}`

    }else {
      alert("please enter the valid id")
    }
   
  }
  return (
    <div className='GetUser'>
      <input placeholder='enter a userid' onChange={handleEvent}value={inputValue}></input>
      <button onClick={handleNum}>Get</button>
      
    </div>
  );
}


function DelUsers() {
  const [inputValue, setInputValue] = useState();

  const handleEvent = (event) =>  {
    setInputValue(event.target.value);
  }

  const handleNum = async () => {
    if (inputValue){
        const response = await axios.delete (`http://localhost:8000/user/delete/${inputValue}`)
        alert("Item has deleted sucessfully")

    }else {
      alert("please enter the valid id")
    }
   
  }
  return (
    <div className='DelUser'>
      <input placeholder='enter a userid to delete' onChange={handleEvent}value={inputValue}></input>
      <button onClick={handleNum}>Delete </button>
      
    </div>
  );
}

function MyMessage() {
  const [message ,setMessage] = useState("Loading....");
  useEffect(() => {
    fetch("http://localhost:8000")
      .then(response => response.json())
      .then(data => setMessage(data.message))
  }, []);

  return (
    <div className='message'>
      <h1> {message}</h1>
    </div>
  );

}

function App() {
  return (
    <div className='App'>
      <MyMessage />
      <GetAllUsers />
      <GetUsers />
      <DelUsers />
    </div>
  );
}

export default App
