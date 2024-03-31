import { ReactNode, createContext, useContext, useReducer } from "react";

export enum FileActionType {
  SET_FILE,
  UPLOAD_FILE,
}

type ReducerAction<T, P> = {
  type: T;
  payload?: Partial<P>;
};

type FileContextState = {
  isLoading: boolean;
  file: File | null;
  fileList: File[]; // & {} You can add more information about the challenge inside this type
};

type FileAction = ReducerAction<FileActionType, Partial<FileContextState>>;

type FileDispatch = ({ type, payload }: FileAction) => void;

type FileContextType = {
  state: FileContextState;
  dispatch: FileDispatch;
};

type FileProviderProps = { children: ReactNode };

export const FileContextInitialValues: Partial<FileContextState> = {
  file: null,
  fileList: [],
  isLoading: false,
};

const FileContext = createContext({} as FileContextType);

const FileReducer = (
  state: FileContextState,
  action: FileAction
): FileContextState => {
  switch (action.type) {
    case FileActionType.SET_FILE:
      return { ...state, file: action.payload?.file || null };
    case FileActionType.UPLOAD_FILE:
      state.file && state.fileList.push(state.file);
      return { ...state, file: null };
    default: {
      throw new Error(`Unhandled action type: ${action.type}`);
    }
  }
};

export const FileProvider = ({ children }: FileProviderProps) => {
  const [state, dispatch] = useReducer(
    FileReducer,
    FileContextInitialValues as FileContextState
  );

  return (
    <FileContext.Provider value={{ state, dispatch }}>
      {children}
    </FileContext.Provider>
  );
};

export const useFileContext = () => {
  const context = useContext(FileContext);

  if (context === undefined)
    throw new Error("useFileContext must be used within a FileProvider");

  return context;
};
