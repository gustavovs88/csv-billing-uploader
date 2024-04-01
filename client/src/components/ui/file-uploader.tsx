import { useEffect, useState } from "react";
import { useFileContext, FileActionType, SubmittedFiles } from "./file";
import fetchClient from "@/lib/fetchClient";
import { LoadingSpinner } from "./load-spinner";

type FileUploaderProps = {
  label?: string;
};

const FileUploader = ({ label }: FileUploaderProps) => {
  const { state, dispatch } = useFileContext();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const handleFileChange = (event: Event) => {
      const target = event.target as HTMLInputElement;
      const selectedFile = target.files && target.files[0];
      if (selectedFile) {
        dispatch({
          type: FileActionType.SET_FILE,
          payload: { file: selectedFile },
        });
      }
    };

    const fileInput = document.getElementById("file") as HTMLInputElement;
    fileInput.addEventListener("change", handleFileChange);

    return () => {
      fileInput.removeEventListener("change", handleFileChange);
    };
  }, [dispatch]);

  const handleSubmit = async (file: File | null) => {
    setIsLoading(true);
    try {
      if (!file) return;
      const submitFile = await fetchClient.postFile(
        "/billings/csv/upload",
        file
      );
      if (!submitFile.ok) {
        setIsLoading(false);
        throw new Error("Erro ao submeter o arquivo");
      }
      dispatch({ type: FileActionType.UPLOAD_FILE });
      const submittedFiles: { records: SubmittedFiles[] } =
        await fetchClient.get("/billings/csv/uploads");
      if ("error" in submittedFiles) {
        alert("Erro ao buscar arquivos submetidos");
        setIsLoading(false);
      } else {
        dispatch({
          type: FileActionType.GET_SUBMITTED_FILES,
          payload: { submittedFiles: submittedFiles.records },
        });
      }

      setIsLoading(false);
    } catch (error) {
      alert("Erro ao submeter o arquivo");
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 bg-zinc-800 p-6">
      <div>
        <input
          id="file"
          type="file"
          accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,text/csv"
          className="hidden"
        />
        <label
          htmlFor="file"
          className="bg-indigo-500 hover:bg-indigo-600 text-white font-semibold px-4 py-2 rounded-lg shadow-sm cursor-pointer"
        >
          {label || "Inserir arquivo"}
        </label>
      </div>
      {state.file && (
        <section className="text-white animate-accordion-down">
          <p className="pb-6 font-bold">Detalhes do arquivo:</p>
          <ul className="indent-4">
            <li>Nome: {state.file.name}</li>
            <li>Tipo: {state.file.type}</li>
            <li>Tamanho: {state.file.size} bytes</li>
          </ul>
        </section>
      )}

      {state.file && (
        <button
          className="rounded-lg bg-green-800 text-white px-4 py-2 border-none font-semibold max-w-md"
          onClick={() => {
            handleSubmit(state.file);
          }}
        >
          {isLoading ? (
            <LoadingSpinner size="sm"></LoadingSpinner>
          ) : (
            "Submeter arquivo"
          )}
        </button>
      )}
    </div>
  );
};

export { FileUploader };
