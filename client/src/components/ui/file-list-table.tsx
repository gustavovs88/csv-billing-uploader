import {
  Table,
  TableHeader,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TableCaption,
} from "./table";
import { useFileContext } from "./file";
import { useEffect } from "react";

const FileListTable = () => {
  const { state } = useFileContext();
  useEffect(() => {
    console.log(state.fileList);
  }, [state.fileList]);

  return (
    <div className="overflow-x-auto">
      {!!state.fileList.length && (
        <Table className="min-w-full divide-y divide-gray-200">
          <TableCaption>Lista de arquivos submetidos</TableCaption>
          <TableHeader>
            <TableRow key={""}>
              <TableHead>Nome</TableHead>
              <TableHead>Tamanho (bytes)</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {state.fileList.map((file, index) => (
              <TableRow key={index}>
                <TableCell>{file.name}</TableCell>
                <TableCell>{file.size}</TableCell>
                <TableCell>Submitted</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
};

export { FileListTable };
