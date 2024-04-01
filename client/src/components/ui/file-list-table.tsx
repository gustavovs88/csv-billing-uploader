import {
  Table,
  TableHeader,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TableCaption,
} from "./table";
import {
  FileActionType,
  ClientFileSubmittedStatus,
  SubmittedFiles,
  useFileContext,
} from "./file";
import { useEffect, useState } from "react";
import { LoadingSpinner } from "./load-spinner";
import fetchClient from "@/lib/fetchClient";
import { formatDate } from "@/lib/utils";

const FileListTable = () => {
  const { state, dispatch } = useFileContext();
  const [isLoading, setIsLoading] = useState(false);

  // eslint-disable-next-line @typescript-eslint/no-empty-function
  useEffect(() => {}, [state.submittedFiles]); //Re-renders on submittedFiles update

  const handleUpdate = async () => {
    setIsLoading(true);
    const submittedFiles: { records: SubmittedFiles[] } = await fetchClient.get(
      "/billings/csv/uploads"
    );
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
  };

  return (
    <div className="flex flex-col justify-center items-center p-16">
      {!!state.submittedFiles.length && (
        <Table className="min-w-full divide-y divide-gray-200 mb-3">
          <TableCaption>Lista de arquivos submetidos</TableCaption>
          <TableHeader>
            <TableRow key={""}>
              <TableHead>Nome</TableHead>
              <TableHead>Enviado em</TableHead>
              <TableHead>Última atualização em</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {state.submittedFiles.map((file, index) => (
              <TableRow key={index}>
                <TableCell>{file.name}</TableCell>
                <TableCell>{formatDate(file.createdat)}</TableCell>
                <TableCell>{formatDate(file.updatedat)}</TableCell>
                <TableCell>{ClientFileSubmittedStatus[file.status]}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
      {!!state.submittedFiles.length && (
        <button
          disabled={isLoading}
          className="rounded-lg bg-green-800 text-white px-4 py-2 border-none font-semibold max-w-md"
          onClick={() => {
            handleUpdate();
          }}
        >
          {isLoading ? (
            <LoadingSpinner size="sm"></LoadingSpinner>
          ) : (
            "Atualizar lista"
          )}
        </button>
      )}
    </div>
  );
};

export { FileListTable };
