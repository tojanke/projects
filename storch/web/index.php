
<html>
<head>
    <link rel="stylesheet" type="text/css" href="css/main.css" />        
    <title>Storch</title>
    <?php    
    include_once 'dbConfig.php';
    $currentDate = new DateTime();    
    if(isset($_GET['day'])){        
        $currentDate->sub(new DateInterval("P" . $_GET['day'] . "D"));        
    }
    $currentDay = $currentDate->format('Y-m-d');
    ?>
</head>
<body>
    <div id="header-container">
        <img src="img/storch.png"/>
    </div>    
    <div id="main-container">        
        <div id="selector-container">
            <?php
                $tempDate = new DateTime();
                $tempDate->sub(new DateInterval("P6D"));                
            ?>
            <a href="?day=6"><?php echo $tempDate->format("d.m.Y") ?></a>
            <?php $tempDate->add(new DateInterval("P1D")) ?>
            <a href="?day=5"><?php echo $tempDate->format("d.m.Y") ?></a>
            <?php $tempDate->add(new DateInterval("P1D")) ?>
            <a href="?day=4"><?php echo $tempDate->format("d.m.Y") ?></a>
            <?php $tempDate->add(new DateInterval("P1D")) ?>
            <a href="?day=3"><?php echo $tempDate->format("d.m.Y") ?></a>
            <?php $tempDate->add(new DateInterval("P1D")) ?>
            <a href="?day=2"><?php echo $tempDate->format("d.m.Y") ?></a>
            <?php $tempDate->add(new DateInterval("P1D")) ?>
            <a href="?day=1"><?php echo $tempDate->format("d.m.Y") ?></a>
            <?php $tempDate->add(new DateInterval("P1D")) ?>
            <a href="?day=0"><?php echo $tempDate->format("d.m.Y") ?></a>
        </div>
        <div id="content-container">
            <?php
                $sql = "SELECT idframes, time, thumbnail FROM frames where time > \"" . $currentDay . " 00:00\" and time < \"" . $currentDay . " 23:59\" order by time asc";                
                $result = $conn->query($sql);

                if ($result->num_rows > 0) {        
                    while($row = $result->fetch_assoc()) {
                        echo "<a href=\"\"><img src=\"data:image/jpeg;base64," . $row["thumbnail"] . "\" title=\"" . $row["time"] . "\"/></a>";
                    }
                }              
                $conn->close();
            ?>
        </div>
    </div>    
</body>
</html>

