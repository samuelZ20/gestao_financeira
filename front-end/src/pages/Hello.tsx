import { useEffect, useState } from "react";
import { api } from "../api/api"

export default function Hello() {
    const [mensagem, setMensagem] = useState("Carregando...");

    useEffect(() => {
        api
            .get("/hello")
            .then((res) => setMensagem(res.data.mensagem))
            .catch(() => setMensagem("Erro ao conectar com o back"));
    }, []);

    return <h1>{mensagem}</h1>;
}