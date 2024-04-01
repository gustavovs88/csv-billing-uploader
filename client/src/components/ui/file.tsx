import { ReactNode, createContext, useContext, useReducer } from "react";

export enum FileActionType {
  SET_FILE,
  UPLOAD_FILE,
  GET_SUBMITTED_FILES,
}

export enum ServerFileSubmittedStatus {
  ACKNOWLEDGED = "ACKNOWLEDGED",
  SENT = "SENT",
}

export enum ClientFileSubmittedStatus {
  ACKNOWLEDGED = "Processando",
  SENT = "Concluído",
}

type ReducerAction<T, P> = {
  type: T;
  payload?: Partial<P>;
};

export interface SubmittedFiles {
  id: number;
  name: string;
  createdat: string;
  updatedat: string;
  status: ServerFileSubmittedStatus;
}

type FileContextState = {
  isLoading: boolean;
  file: File | null;
  submittedFiles: SubmittedFiles[]; // & {} You can add more information about the challenge inside this type
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
  submittedFiles: [],
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
      return { ...state, file: null };
    case FileActionType.GET_SUBMITTED_FILES:
      return { ...state, submittedFiles: action.payload?.submittedFiles || [] };
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
