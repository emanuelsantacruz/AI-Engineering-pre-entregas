import json
import os
from rag_system import RAGSystem

def evaluate():
    golden_path = os.path.join(os.path.dirname(__file__), "golden_set.json")
    with open(golden_path, "r", encoding="utf-8") as f:
        golden_set = json.load(f)

    rag = RAGSystem()

    total_queries = len(golden_set)
    hits = 0

    print("=== Evaluando Recuperador Híbrido (BM25 + Pinecone) ===\n")
    print(f"{'Pregunta':<65} | {'Esperado':<16} | {'Encontrado Top-5'}")
    print("-" * 105)

    for item in golden_set:
        pregunta = item["pregunta"]
        esperado = item["doc_id_esperado"]

        recuperados = rag.get_top_documents(pregunta)
        ids_recuperados = [d.metadata.get("doc_id") for d in recuperados]

        acierto = esperado in ids_recuperados
        if acierto:
            hits += 1

        print(f"{pregunta[:62] + '...':<65} | {esperado:<16} | {'SI' if acierto else 'NO'}")

    recall_at_5 = hits / total_queries
    precision_at_5 = (hits / (total_queries * 5))

    print("\n" + "=" * 45)
    print("REPORTE DE EVALUACIÓN")
    print("=" * 45)
    print(f"Total de consultas: {total_queries}")
    print(f"Aciertos en Top-5:  {hits}/{total_queries}")
    print(f"Recall@5:           {recall_at_5:.2%}")
    print(f"Precision@5:        {precision_at_5:.2%}")
    print("=" * 45)

if __name__ == "__main__":
    evaluate()
