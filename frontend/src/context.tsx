import React from 'react';

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

export const initialValue = {
	token: '',
	authUserId: -1
}

export const Context = React.createContext<IContext>({ getters: initialValue });
export const useContext = React.useContext;