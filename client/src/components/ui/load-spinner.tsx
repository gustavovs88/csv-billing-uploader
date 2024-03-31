import clsx from "clsx";

export interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

const LoadingSpinner = ({ size = "sm", className }: LoadingSpinnerProps) => {
  return (
    <div
      className={clsx(
        "grid justify-center items-center animate-spin ",
        {
          "h-6": size === "sm",
          "h-8": size === "md",
          "h-10": size === "lg",
        },
        className
      )}
    >
      <div
        className={clsx(
          "border-t-black border-t-4 border-4 border-gray-800 rounded-full",
          {
            "h-6 w-6 border-t-4 border-4": size === "sm",
            "h-8 w-8 border-t-4 border-4": size === "md",
            "h-10 w-10 border-t-8 border-8": size === "lg",
          },
          className
        )}
      ></div>
    </div>
  );
};

export { LoadingSpinner };
