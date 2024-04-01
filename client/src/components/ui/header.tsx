import logo from "../../assets/logo.webp";

const Header = ({ ...props }) => {
  return (
    <header
      className="flex flex-col items-start justify-center p-8 h-8 w-full"
      {...props}
    >
      <img src={logo} className="w-32"></img>
    </header>
  );
};

export { Header };
