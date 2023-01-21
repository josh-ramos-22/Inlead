import React from "react";

interface IContext {
	getters : {
		token: string;
		authUserId : number
	};

	setters?: {
		setToken?: (newToken : string ) => void;
		setUID?: (authUserId : number) => void
	}
}

const initToken = localStorage.getItem("token");
const initUID = localStorage.getItem("auth_user_id");

export const initialValue = {
  token: initToken !== null ? initToken : "",
  authUserId: initUID !== null ? JSON.parse(initUID) : -1
};

export const Context = React.createContext<IContext>({ getters: initialValue });
export const useContext = React.useContext;