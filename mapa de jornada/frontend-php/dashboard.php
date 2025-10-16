<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Mapa de Jornada</title>
    <link rel="stylesheet" href="dashboard.css">
</head>
<body>
    <div class="dashboard-container">
        <h1>Meu Mapa de Jornada</h1>

        <a href="index.php" class="link-voltar">⬅ Voltar ao Questionário</a>
        
        <main class="journey-grid">
            <div class="grid-header">Semana 1</div>
            <div class="grid-header">Semana 2</div>
            <div class="grid-header">Semana 3</div>
            <div class="grid-header">Semana 4</div>

            <div class="grid-label">Emoção predominante</div>
            <div class="grid-cell" data-semana="1" data-tipo="emocao"></div>
            <div class="grid-cell" data-semana="2" data-tipo="emocao"></div>
            <div class="grid-cell" data-semana="3" data-tipo="emocao"></div>
            <div class="grid-cell" data-semana="4" data-tipo="emocao"></div>

            <div class="grid-label">Nível de desejo de uso</div>
            <div class="grid-cell" data-semana="1" data-tipo="desejo"></div>
            <div class="grid-cell" data-semana="2" data-tipo="desejo"></div>
            <div class="grid-cell" data-semana="3" data-tipo="desejo"></div>
            <div class="grid-cell" data-semana="4" data-tipo="desejo"></div>

            <div class="grid-label">Ações de autocuidado</div>
            <div class="grid-cell" data-semana="1" data-tipo="autocuidado"></div>
            <div class="grid-cell" data-semana="2" data-tipo="autocuidado"></div>
            <div class="grid-cell" data-semana="3" data-tipo="autocuidado"></div>
            <div class="grid-cell" data-semana="4" data-tipo="autocuidado"></div>

            <div class="grid-label">Dificuldade principal</div>
            <div class="grid-cell" data-semana="1" data-tipo="dificuldade"></div>
            <div class="grid-cell" data-semana="2" data-tipo="dificuldade"></div>
            <div class="grid-cell" data-semana="3" data-tipo="dificuldade"></div>
            <div class="grid-cell" data-semana="4" data-tipo="dificuldade"></div>
        </main>
    </div>
    <script src="dashboard.js"></script>
</body>
</html>