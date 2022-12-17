import React from "react";
import ReactDOM from "react-dom";
import {default as url} from "./backendurl";
import {useEffect, useState, useRef} from "react";

import "./styles.css";

export function Login() {
  // React States
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  let [response, setResponse] = useState()
  let formRef = useRef(null)

  // User Login info

  const errors = {
    inputUsername: "invalid username",
    inputPassword: "invalid password"
  };

  const handleSubmit = async (event) => {
    //Prevent page reload
    event.preventDefault();

    let inputUsername = formRef.current.inputUsername.value;
    let inputPassword = formRef.current.inputPassword.value;


    // Find user login info
    let response = await fetch(url + "/login?inputUsername=" + inputUsername + "&inputPassword=" + inputPassword)
    .then(response => localStorage.setItem("token", response.text()))
    .catch( error => setErrorMessages({ name: "inputPassword", message: errors.inputPassword }))

  };

  // Generate JSX code for error message
  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error">{errorMessages.message}</div>
    );

  // JSX code for login form
  const renderForm = (
    <div className="form">
      <form onSubmit={handleSubmit} ref = {formRef}>
        <div className="input-container">
          <label>Username </label>
          <input type="text" name="inputUsername" required />
          {renderErrorMessage("inputUsername")}
        </div>
        <div className="input-container">
          <label>Password </label>
          <input type="password" name="inputPassword" required />
          {renderErrorMessage("inputPassword")}
        </div>
        <div className="button-container">
          <input type="submit" value="Log In" />
        </div>
      </form>
    </div>
  );

  return (
    <div className="login">
      <div className="login-form">
        <div className="title">Log In</div>
        {isSubmitted ? <div>User is successfully logged in</div> : renderForm}
      </div>
    </div>
  );
}
