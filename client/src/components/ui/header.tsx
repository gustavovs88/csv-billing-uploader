import logo from "../../assets/logo.webp";

const Header = ({ ...props }) => {
  return (
    <header
      className="flex flex-col items-start justify-center p-4 h-8 w-full"
      {...props}
    >
      <img src={logo} className="w-20"></img>
    </header>
  );
};

export { Header };
