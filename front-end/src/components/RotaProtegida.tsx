// RN17: só mostra a tela se houver alguém logado; senão, manda para o login.
import type { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/authContext'

export default function RotaProtegida({ children }: { children: ReactNode }) {
  const { estaLogado } = useAuth()
  if (!estaLogado) {
    return <Navigate to="/login" replace />
  }
  return children
}